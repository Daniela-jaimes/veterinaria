# API de Clínica Veterinaria (backend)

API REST para gestionar una clínica veterinaria: clientes, mascotas, veterinarios, citas, consultas, historias clínicas, tratamientos y vacunación. Incluye autenticación con JWT y control de acceso por rol.

## Tecnologías

- Python 3.12+
- FastAPI + Uvicorn
- SQLAlchemy 2 (async) + asyncpg
- PostgreSQL (Neon)
- Pydantic v2 / pydantic-settings
- JWT con PyJWT, hash de contraseñas con bcrypt

## Estructura

```
veterinaria
  backend/
  ├── .env.example        # plantilla de variables de entorno
  ├── requirements.txt
  ├── seed.py             # datos de ejemplo para pruebas
  └── app/
      ├── main.py         # app FastAPI, CORS, routers
      ├── core/           # config, conexión a BD, seguridad    (JWT/bcrypt), excepciones
      ├── models/         # modelos SQLAlchemy (un archivo por tabla) y enums
      ├── schemas/        # schemas Pydantic (entrada/salida)
      ├── repositories/   # acceso a datos
      ├── services/       # lógica de negocio y transacciones
      └── routers/        # endpoints HTTP
```

Flujo de una petición: `router → service → repository → modelo`. Los repositorios hacen `flush`; el commit lo controla el servicio.

## Instalación

Desde la carpeta `veterinaria/backend/`:

```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Configuración



| Variable | Obligatoria | Descripción |
|---|---|---|
| `DATABASE_URL` | Sí | Cadena de conexión a PostgreSQL (se convierte internamente a `postgresql+asyncpg`). |
| `SECRET_KEY` | Sí | Clave para firmar los JWT. Genérala con `python -c "import secrets; print(secrets.token_urlsafe(48))"`. |
| `CORS_ORIGINS` | No | Orígenes permitidos separados por coma. Por defecto `http://localhost:4200`. |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | No | Duración del token. Por defecto `60`. |

> `.env` contiene secretos: no lo subas a git ni lo incluyas en entregas.

## Base de datos

La API espera que las tablas y los tipos enum de PostgreSQL ya existan en la BD:

- Tablas: `customer`, `pet`, `breed`, `pet_allergy`, `veterinarian`, `speciality`, `appointment`, `medical_record`, `consultation`, `treatment`, `medication`, `vaccine`, `vaccination`, `app_user`.
- Tipos enum: `pet_species`, `pet_sex`, `appointment_status`, `treatment_status`, `consultation_type`, `user_role`.

## Ejecutar

```powershell
uvicorn app.main:app --reload
```

- Documentación interactiva: http://127.0.0.1:8000/docs
- Comprobar la conexión a la BD: http://127.0.0.1:8000/db-test

## Datos de ejemplo

```powershell
python seed.py
```

Carga especialidades, veterinarios, clientes, razas, mascotas, alergias, historias clínicas, medicamentos, vacunas, citas, una consulta con tratamiento y vacunación, y usuarios. Es idempotente: se puede ejecutar varias veces sin duplicar datos.

Usuarios de ejemplo (contraseña `Admin123!`; cámbiala si vas a desplegar):

| Usuario | Rol |
|---|---|
| `admin` | admin |
| `recepcion` | receptionist |
| `dra.gomez` | veterinarian |

## Autenticación

1. `POST /auth/login` con `username` y `password` como formulario (`application/x-www-form-urlencoded`). Devuelve `access_token`.
2. Envía el token en cada petición: `Authorization: Bearer <access_token>`.
3. En `/docs`, el botón **Authorize** hace estos pasos por ti.

Acceso:

- `/`, `/db-test` y `/auth/login`: públicos.
- Todos los recursos de datos: cualquier usuario autenticado.
- `/users`: solo rol `admin` (403 para los demás).

## Endpoints

Cada recurso ofrece `POST`, `GET` (lista paginada), `GET /{id}`, `PUT /{id}` y `DELETE /{id}`.

| Recurso | Ruta | `DELETE` |
|---|---|---|
| Clientes | `/customers` | Lógico (`is_active=false`). 409 si tiene mascotas activas. |
| Mascotas | `/pets` | Lógico (`is_active=false`). |
| Alergias | `/pet-allergies` | Físico. |
| Razas | `/breeds` | Físico. 409 si hay mascotas con esa raza. |
| Veterinarios | `/veterinarians` | Lógico (`is_active=false`). |
| Especialidades | `/specialities` | Físico. 409 si hay veterinarios asociados. |
| Citas | `/appointments` | Pasa a `cancelled`. 409 si está completada o en no-show. |
| Historias clínicas | `/medical-records` | Físico. 409 si tiene consultas. |
| Consultas | `/consultations` | Físico. 409 si tiene tratamientos o vacunaciones. |
| Tratamientos | `/treatments` | Pasa a `suspended`. 409 si ya está completado. |
| Medicamentos | `/medications` | Físico. 409 si se usa en tratamientos. |
| Vacunas | `/vaccines` | Físico. 409 si tiene vacunaciones. |
| Vacunaciones | `/vaccinations` | Físico. |
| Usuarios | `/users` | Lógico (`is_active=false`). |
| Auth | `/auth/login`, `/auth/me` | — |

Los listados aceptan `limit` (1–100, por defecto 20) y `offset`, y responden:

```json
{ "items": [], "total": 0, "limit": 20, "offset": 0 }
```

## Reglas de negocio

- **Citas:** un veterinario no puede tener dos citas activas (`scheduled` o `in_consultation`) que se solapen. Las transiciones de estado permitidas son `scheduled → in_consultation / cancelled / no_show` e `in_consultation → completed / cancelled`. Solo se reprograma una cita `scheduled`.
- **Historias clínicas:** una por mascota.
- **Consultas:** una por cita; la cita debe corresponder a la misma mascota de la historia clínica. Al crear la consulta, la cita `scheduled` pasa a `in_consultation`.
- **Vacunaciones:** no se repite la misma vacuna en una consulta.
- **Clientes y mascotas:** email y microchip únicos. Un cliente con mascotas activas no se puede desactivar.
- **Usuarios:** username y email únicos; un veterinario solo puede tener un usuario; el rol `veterinarian` exige `vet_id`.

## Códigos de error

| Código | Cuándo |
|---|---|
| 400 | Regla de negocio incumplida (estado, inactivo, fechas). |
| 401 | Falta el token, es inválido/expirado o las credenciales son incorrectas. |
| 403 | El rol no tiene permiso. |
| 404 | El recurso o una referencia no existe. |
| 409 | Duplicado o conflicto de integridad (unicidad, solapamiento, FK con `RESTRICT`). |
| 422 | Datos de entrada inválidos. |

## Formatos

- Fechas: `AAAA-MM-DD` (por ejemplo `2026-09-06`, con ceros).
- Fecha y hora: `AAAA-MM-DDTHH:MM:SS`.
- Enums: valores en minúscula (`scheduled`, `dog`, `male`, `admin`, …).
- Contraseñas: de 8 a 72 bytes.
