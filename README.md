# Seynurwa - Simple Authentication API

Sistema de autenticación simple con registro y login de usuarios, desplegable en Vercel.

## 🚀 Quick Start Local

### 1. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 2. Configurar Base de Datos

```bash
# Con Docker
docker run --name auth-db \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=authdb \
  -p 5432:5432 \
  -d postgres:15

# Configurar variables de entorno
export DATABASE_URL="postgresql+asyncpg://postgres:postgres@localhost:5432/authdb"
export JWT_SECRET="mi-secreto-local"
```

### 3. Ejecutar Migraciones

```bash
alembic upgrade head
```

### 4. Iniciar Servidor

```bash
uvicorn api.index:app --reload
```

API disponible en `http://localhost:8000`

## 📡 Endpoints

### POST `/api/register`

Registrar nuevo usuario.

```bash
curl -X POST http://localhost:8000/api/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "email": "test@example.com",
    "password": "password123"
  }'
```

### POST `/api/login`

Login y obtener token JWT.

```bash
curl -X POST http://localhost:8000/api/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123"
  }'
```

## ☁️ Despliegue en Vercel

### 1. Instalar Vercel CLI

```bash
npm i -g vercel
```

### 2. Login

```bash
vercel login
```

### 3. Preparar Base de Datos

Necesitas una base de datos PostgreSQL accesible desde internet. Opciones recomendadas:

- **Neon** (https://neon.tech) - Gratis, serverless
- **Supabase** (https://supabase.com) - Gratis, fácil setup
- **Railway** (https://railway.app) - Simple deployment

### 4. Desplegar

```bash
vercel
```

### 5. Configurar Variables de Entorno

En el dashboard de Vercel, añade:

- `DATABASE_URL` - URL de tu base de datos PostgreSQL
- `JWT_SECRET` - Secreto para firmar tokens JWT

### 6. Ejecutar Migraciones en Producción

```bash
# Conectarte a tu base de datos de producción
export DATABASE_URL="postgresql+asyncpg://..."
alembic upgrade head
```

## 📁 Estructura del Proyecto

```
seynurwa/
├── api/
│   └── index.py              # Entry point para Vercel
├── auth/
│   ├── domain/               # Lógica de negocio pura
│   ├── application/          # Casos de uso y DTOs
│   └── infrastructure/       # Base de datos y API
├── alembic/                  # Migraciones (raíz del proyecto)
├── vercel.json               # Configuración de Vercel
└── requirements.txt
```

## 🔐 Seguridad

- Contraseñas hasheadas con bcrypt
- JWT tokens firmados con HS256
- Validación de email
- Mínimo 8 caracteres para contraseñas

## 📝 Variables de Entorno

| Variable | Required | Description |
|----------|----------|-------------|
| `DATABASE_URL` | Yes | PostgreSQL connection string |
| `JWT_SECRET` | Yes | Secret for signing JWT tokens |
| `JWT_EXPIRATION_HOURS` | No | Token expiration (default: 24) |
