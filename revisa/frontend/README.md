# Frontend Angular — Clínica Veterinaria

Frontend standalone Angular conectado al backend FastAPI del proyecto.

## Incluye
- Login con `POST /auth/login` usando `application/x-www-form-urlencoded`.
- Persistencia del JWT en `localStorage`.
- Interceptor HTTP que agrega `Authorization: Bearer <token>` automáticamente.
- Redirección al login cuando la API devuelve 401.
- Guard de autenticación y guard de administrador para `/users`.
- Paginación basada directamente en `{ items, total, limit, offset }`.
- CRUD de clientes, mascotas y citas.
- Navegación/listado para el resto de módulos del backend.
- Diseño responsive sin dependencias de UI externas.

## Ejecutar

1. Levanta el backend en `http://127.0.0.1:8000`.
2. Desde `frontend/` ejecuta:

```bash
npm install
npm start
```

3. Abre `http://localhost:4200`.
4. Usuarios de prueba del seed: `admin`, `recepcion`, `dra.gomez`; contraseña `Admin123!`.

La URL de la API se configura en `src/environments/environment.ts`.
