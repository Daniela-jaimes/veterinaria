# Clínica Veterinaria (frontend)

Aplicación web para gestionar una clínica veterinaria: clientes, mascotas, veterinarios, citas, consultas, historias clínicas, tratamientos y vacunación. Consume la API REST del backend e incluye inicio de sesión con JWT y vistas según el rol del usuario.

## Tecnologías

- Angular 17+ (TypeScript, componentes standalone)
- Node.js 20+ y npm
- RxJS
- HttpClient con interceptor para el token JWT
- Guards de rutas para autenticación y rol

> Ajusta esta lista a lo que uses realmente (librería de UI, versión exacta de Angular, etc.).

## Estructura

```
veterinaria
  frontend/
  ├── angular.json
  ├── package.json
  ├── tsconfig.json
  ├── tsconfig.app.json
  └── src/
      ├── index.html
      ├── main.ts               # arranque de la aplicación
      ├── styles.css            # estilos globales
      ├── environments/         # URL de la API por entorno
      └── app/
          ├── app.component.ts  # componente raíz
          ├── app.routes.ts     # rutas de la aplicación
          ├── core/
          │   ├── guards/       # protección de rutas (sesión y rol)
          │   ├── interceptors/ # token JWT y manejo de errores HTTP
          │   ├── models/       # interfaces y tipos (entidades, enums)
          │   └── services/     # comunicación con la API
          ├── layout/           # estructura común (menú, cabecera)
          └── pages/
              ├── login/
              ├── dashboard/
              ├── customers/
              ├── pets/
              ├── appointments/
              └── resource-list/  # listado reutilizable para otros recursos
```

Flujo de una pantalla: `page → service → API (HttpClient)`. El interceptor agrega el token a cada petición y, si la API responde 401, limpia la sesión y redirige al login.

## Requisitos previos

- Node.js 20+ y npm.
- El backend en ejecución (ver el README del backend). Por defecto en `http://127.0.0.1:8000`.

## Instalación

Desde la carpeta `veterinaria/frontend/`:

```powershell
npm install
```

## Configuración

La URL de la API se define en `src/environments/`:

| Archivo | Uso | Propiedad |
|---|---|---|
| `environment.ts` | Desarrollo | `apiUrl: 'http://127.0.0.1:8000'` |
| `environment.prod.ts` | Producción | `apiUrl: '<URL del backend desplegado>'` |

> El backend debe permitir el origen del frontend en `CORS_ORIGINS` (por defecto `http://localhost:4200`).

## Ejecutar

```powershell
npm start
```

(equivale a `ng serve`). La aplicación queda en http://localhost:4200.

## Comandos útiles

| Comando | Descripción |
|---|---|
| `npm start` | Servidor de desarrollo con recarga automática. |
| `npm run build` | Compilación de producción en `dist/`. |
| `npm test` | Pruebas unitarias. |

## Autenticación

1. En la pantalla de inicio de sesión, ingresa `username` y `password`. El frontend llama a `POST /auth/login` y guarda el `access_token`.
2. El interceptor envía `Authorization: Bearer <access_token>` en cada petición.
3. Si el token falta, es inválido o expiró (401), se limpia la sesión y se redirige al login.
4. Al cerrar sesión se elimina el token almacenado.

Usuarios de ejemplo (cargados con `python seed.py` en el backend; contraseña `Admin123!`):

| Usuario | Rol |
|---|---|
| `admin` | admin |
| `recepcion` | receptionist |
| `dra.gomez` | veterinarian |

## Acceso por rol

- `login`: público.
- Resto de pantallas: solo usuarios autenticados (guard de sesión).
- Gestión de usuarios: solo rol `admin`.

> El control del frontend es solo de experiencia de usuario; la seguridad real la aplica el backend (403).

## Pages

| Page | Carpeta | Descripción |
|---|---|---|
| Inicio de sesión | `pages/login` | Autenticación con usuario y contraseña. |
| Dashboard | `pages/dashboard` | Pantalla de inicio con el resumen de la clínica. |
| Clientes | `pages/customers` | Listado paginado, alta, edición y desactivación. |
| Mascotas | `pages/pets` | Datos de la mascota, raza y alergias. |
| Citas | `pages/appointments` | Agenda, cambio de estado y reprogramación. |
| Listado de recursos | `pages/resource-list` | Listado reutilizable para los demás recursos de la API (razas, especialidades, medicamentos, vacunas, etc.). |

> Ajusta esta tabla a la funcionalidad real de cada page y agrega las rutas definidas en `app.routes.ts`.

## Reglas que se reflejan en la interfaz

- **Citas:** el estado solo avanza por transiciones válidas (`scheduled → in_consultation / cancelled / no_show`, `in_consultation → completed / cancelled`). Solo se reprograma una cita `scheduled`. Un veterinario no puede tener citas activas solapadas.
- **Historias clínicas:** una por mascota.
- **Consultas:** una por cita, y la cita debe ser de la misma mascota de la historia clínica.
- **Vacunaciones:** no se repite la misma vacuna en una consulta.
- **Clientes y mascotas:** email y microchip únicos. Un cliente con mascotas activas no se puede desactivar.
- **Eliminaciones:** algunas son lógicas (`is_active=false`) y otras físicas; la API responde 409 si hay registros relacionados.

## Manejo de errores

La interfaz muestra un mensaje según el código que devuelve la API:

| Código | Qué ve el usuario |
|---|---|
| 400 | Mensaje de la regla de negocio incumplida. |
| 401 | Se redirige al login. |
| 403 | Aviso de que no tiene permiso. |
| 404 | El recurso no existe. |
| 409 | Aviso de duplicado o conflicto (por ejemplo, solapamiento de citas). |
| 422 | Se marcan los campos inválidos del formulario. |

## Formatos

- Fechas enviadas a la API: `AAAA-MM-DD` (por ejemplo `2026-09-06`).
- Fecha y hora: `AAAA-MM-DDTHH:MM:SS`.
- Enums: valores en minúscula (`scheduled`, `dog`, `male`, `admin`, …).
- Contraseñas: de 8 a 72 bytes.

> No subas archivos con secretos ni URLs privadas de producción al repositorio.