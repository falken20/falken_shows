# Guia de pruebas locales - Live Memories

Este documento explica como levantar y validar la aplicacion en local.

## 1. Requisitos previos

- macOS o Linux
- Python 3.11+
- uv instalado
- Node.js 20+ y npm
- Docker + Docker Compose (opcional)

Comprobacion rapida:

```bash
python3 --version
uv --version
node --version
npm --version
docker --version
```

## 2. Configurar variables de entorno

Desde la raiz del repositorio:

```bash
cp .env.example .env
```

## 3. Instalacion de dependencias

### Opcion recomendada (monorepo)

```bash
make install
```

### Si npm falla por registry corporativo (ENOTFOUND artifactory...)

Forzar registry publico solo para este proyecto frontend:

```bash
cd frontend
printf "registry=https://registry.npmjs.org\n" > .npmrc
npm install --no-audit --no-fund
cd ..
```

## 4. Preparar base de datos

Aplicar migraciones:

```bash
make migrate
```

Cargar datos de ejemplo (opcional):

```bash
make seed
```

## 5. Levantar la aplicacion (sin Docker)

En terminal 1 (backend):

```bash
make dev-backend
```

En terminal 2 (frontend):

```bash
make dev-frontend
```

URLs esperadas:

- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- Swagger: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 6. Smoke test funcional rapido

Con backend arriba, verificar salud:

```bash
curl -i http://localhost:8000/api/v1/health
curl -i http://localhost:8000/api/v1/ready
```

Resultado esperado en ambos casos:

- HTTP 200
- JSON con estado `ok`

## 7. Ejecutar pruebas automatizadas

### Todo el proyecto

```bash
make test
```

### Solo backend

```bash
make test-backend
```

### Solo frontend

```bash
make test-frontend
```

### E2E (Playwright)

```bash
make test-e2e
```

## 8. Validaciones de calidad

```bash
make lint
make typecheck
make format
```

## 9. Ejecucion con Docker (alternativa)

Levantar todo con SQLite:

```bash
docker compose up --build -d
```

Levantar con perfil PostgreSQL:

```bash
docker compose --profile postgres up --build -d
```

Parar servicios:

```bash
docker compose down
```

## 10. Checklist de cierre

Antes de dar por valida la prueba local:

- Backend responde `health` y `ready` con HTTP 200
- Frontend carga y muestra estado de salud de la API
- `make test` termina sin errores
- `make lint` y `make typecheck` terminan sin errores
- Si usaste Docker, no quedan contenedores huerfanos al finalizar
