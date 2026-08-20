# Live Memories 🎵

> Aplicación web personal para inventariar y recordar todos los conciertos en directo a los que has asistido a lo largo de tu vida.

<!-- TODO: Replace with real screenshots -->
<!-- ![Live Memories Dashboard](docs/screenshots/placeholder-dashboard.png) -->

---

## Características

- 🎤 **Registro completo** de conciertos: fecha, artista, sala, ciudad, precio, valoración, notas personales
- 🖼 **Galería de fotografías** por concierto (entrada, artista, foto del concierto)
- 📊 **Estadísticas y visualizaciones**: conciertos por año, artistas más vistos, mapa de ubicaciones, línea temporal
- 🔍 **Búsqueda, filtros y ordenación** avanzados
- 📅 **Vista en calendario, tarjetas, tabla y cronología**
- 🎵 **Artistas y recintos**: gestión independiente con estadísticas calculadas automáticamente
- 📤 **Importación y exportación** a JSON y CSV
- 🌙 **Modo oscuro / claro**
- 🌍 **Multiidioma** (Español / Inglés)
- ♿ **Accesible** – WCAG 2.1 AA
- 🔒 **Autenticación JWT** – preparada para múltiples usuarios
- 🐳 **Docker Compose** para arrancar todo localmente con un solo comando
- ☁️ **Preparado para Google Cloud Platform**: Cloud Run, Cloud SQL, Cloud Storage, Secret Manager, Terraform

---

## Stack tecnológico

| Capa | Tecnología |
|---|---|
| Frontend | React 18, TypeScript, Vite, React Router v6, TanStack Query, React Hook Form, Zod, Material UI |
| Backend | Python 3.12, FastAPI, SQLAlchemy 2 (async), Alembic, Pydantic 2, Uvicorn |
| Base de datos | SQLite (desarrollo) / PostgreSQL (producción) |
| Testing BE | Pytest, pytest-cov, HTTPX, Faker |
| Testing FE | Vitest, React Testing Library, MSW, Playwright |
| Calidad | Ruff, Mypy, ESLint, Prettier, pre-commit |
| Infra | Docker, Docker Compose, Terraform, Cloud Build, GitHub Actions |
| GCP | Cloud Run, Cloud SQL, Cloud Storage, Artifact Registry, Secret Manager |

---

## Estructura del repositorio

```
live-memories/
├── .github/
│   ├── copilot-instructions.md   # Instrucciones globales para Copilot
│   ├── instructions/             # Instrucciones específicas por dominio
│   ├── agents/                   # Agentes especializados
│   └── workflows/                # GitHub Actions CI/CD
├── backend/                      # API FastAPI
│   ├── app/
│   │   ├── api/v1/               # Routers y endpoints
│   │   ├── core/                 # Config, seguridad, logging
│   │   ├── db/                   # Sesión de base de datos
│   │   ├── models/               # Modelos SQLAlchemy
│   │   ├── schemas/              # Schemas Pydantic
│   │   ├── services/             # Lógica de negocio
│   │   └── repositories/         # Acceso a datos
│   ├── tests/                    # Tests unitarios e integración
│   ├── alembic/                  # Migraciones
│   └── scripts/                  # Seed y utilidades
├── frontend/                     # SPA React
│   ├── src/
│   │   ├── api/                  # Clientes HTTP + hooks TanStack
│   │   ├── components/           # Componentes reutilizables
│   │   ├── pages/                # Páginas / vistas
│   │   ├── hooks/                # Custom hooks
│   │   ├── i18n/                 # Traducciones
│   │   └── types/                # Tipos TypeScript
│   └── e2e/                      # Tests Playwright
├── infrastructure/
│   ├── terraform/                # IaC para GCP
│   └── cloudbuild/               # Pipelines Cloud Build
├── docs/
│   └── adr/                      # Architectural Decision Records
├── scripts/                      # Scripts de utilidad
├── docker-compose.yml
├── Makefile
└── .env.example
```

---

## Requisitos previos

- [Python 3.12+](https://python.org)
- [uv](https://docs.astral.sh/uv/) – gestor de paquetes Python (`pip install uv`)
- [Node.js 20+](https://nodejs.org) y npm
- [Docker](https://docker.com) y Docker Compose (opcional pero recomendado)
- [Make](https://www.gnu.org/software/make/) (disponible en macOS/Linux)

---

## Instalación local sin Docker

### 1. Clonar el repositorio

```bash
git clone https://github.com/[YOUR_GITHUB_USER]/live-memories.git
cd live-memories
```

### 2. Copiar y configurar variables de entorno

```bash
cp .env.example .env
# Edita .env con tu editor preferido
```

### 3. Instalar dependencias

```bash
make install
```

### 4. Aplicar migraciones

```bash
make migrate
```

### 5. Cargar datos de demostración (opcional)

```bash
make seed
```

### 6. Arrancar los servidores

```bash
# En dos terminales separadas:
make dev-backend   # http://localhost:8000
make dev-frontend  # http://localhost:5173
```

---

## Instalación local con Docker

### Usando SQLite (por defecto)

```bash
cp .env.example .env
docker compose up --build -d
```

- Frontend: http://localhost:80
- Backend API: http://localhost:8000
- Swagger UI: http://localhost:8000/docs

### Usando PostgreSQL local

```bash
docker compose --profile postgres up --build -d
```

El backend con PostgreSQL queda expuesto en el puerto `8001`.

---

## Variables de entorno

Todas las variables están documentadas en [`.env.example`](.env.example).

| Variable | Descripción | Por defecto |
|---|---|---|
| `APP_NAME` | Nombre de la aplicación | `Live Memories` |
| `DATABASE_URL` | Cadena de conexión a la base de datos | SQLite local |
| `JWT_SECRET_KEY` | Clave secreta para JWT | *obligatorio en prod* |
| `STORAGE_BACKEND` | `local` o `gcs` | `local` |
| `GCS_BUCKET_NAME` | Nombre del bucket en GCS | - |
| `VITE_API_BASE_URL` | URL de la API para el frontend | `http://localhost:8000/api/v1` |

---

## Base de datos

### SQLite (desarrollo)

```env
DATABASE_URL=sqlite+aiosqlite:///./data/live_memories.db
```

### PostgreSQL (producción)

```env
DATABASE_URL=postgresql+asyncpg://user:password@host:5432/live_memories
```

No es necesario modificar el código para cambiar de motor.

---

## Migraciones

```bash
# Aplicar todas las migraciones pendientes
make migrate

# Crear una nueva migración
make migrate-create MSG="add setlist table"

# Ver historial de migraciones
make migrate-history

# Revertir un paso
make migrate-downgrade
```

---

## Ejecución de tests

```bash
make test              # Todos los tests
make test-backend      # Solo backend (con cobertura)
make test-frontend     # Solo frontend
make test-e2e          # Tests end-to-end con Playwright
```

### Cobertura

```bash
# El informe HTML queda en backend/htmlcov/index.html
make test-backend
open backend/htmlcov/index.html
```

Cobertura mínima requerida: **80 %**

---

## Calidad de código

```bash
make lint       # Ejecutar todos los linters
make format     # Formatear todo el código
make typecheck  # Verificar tipos (Mypy + TypeScript)
```

### Pre-commit hooks

```bash
make pre-commit-install   # Instalar hooks
make pre-commit-run       # Ejecutar en todos los archivos
```

---

## API y documentación OpenAPI

Con el backend en marcha:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

### Endpoints principales

```
GET    /api/v1/health             Health check
GET    /api/v1/ready              Readiness check
GET    /api/v1/concerts           Listado de conciertos (paginado)
POST   /api/v1/concerts           Crear concierto
GET    /api/v1/concerts/{id}      Detalle de concierto
PUT    /api/v1/concerts/{id}      Actualizar concierto completo
PATCH  /api/v1/concerts/{id}      Actualizar concierto parcial
DELETE /api/v1/concerts/{id}      Eliminar concierto
GET    /api/v1/artists            Listado de artistas
POST   /api/v1/artists            Crear artista
GET    /api/v1/venues             Listado de recintos
POST   /api/v1/venues             Crear recinto
POST   /api/v1/uploads            Subir imagen
GET    /api/v1/statistics/summary Estadísticas generales
```

---

## Gestión de imágenes

**Desarrollo (local)**: Las imágenes se almacenan en `./data/uploads/` y se sirven como archivos estáticos.

**Producción (GCS)**: Se usan URLs firmadas con expiración configurable. Las imágenes originales se procesan con Pillow: validación de tipo, generación de miniaturas.

---

## Importación y exportación

```bash
GET  /api/v1/concerts/export?format=json   # Exportar a JSON
GET  /api/v1/concerts/export?format=csv    # Exportar a CSV
POST /api/v1/concerts/import/preview       # Previsualizar importación
POST /api/v1/concerts/import/confirm       # Confirmar importación
```

Plantillas de ejemplo en `scripts/templates/`.

---

## Construcción de imágenes Docker

```bash
docker build -t live-memories-backend:latest backend/
docker build -t live-memories-frontend:latest frontend/
# O con Make:
make build
```

---

## Despliegue en GCP

### Con Terraform

```bash
cd infrastructure/terraform
terraform init
terraform plan -var-file=terraform.tfvars
terraform apply -var-file=terraform.tfvars
```

Ver [`infrastructure/terraform/terraform.tfvars.example`](infrastructure/terraform/terraform.tfvars.example).

### Despliegue manual (Cloud Run)

```bash
gcloud auth configure-docker REGION-docker.pkg.dev
docker build -t REGION-docker.pkg.dev/PROJECT_ID/live-memories/backend:latest backend/
docker push REGION-docker.pkg.dev/PROJECT_ID/live-memories/backend:latest
gcloud run deploy live-memories-backend \
  --image REGION-docker.pkg.dev/PROJECT_ID/live-memories/backend:latest \
  --region REGION \
  --set-secrets="JWT_SECRET_KEY=jwt-secret:latest" \
  --add-cloudsql-instances PROJECT_ID:REGION:INSTANCE_NAME
```

---

## CI/CD

Los workflows de GitHub Actions están en [`.github/workflows/`](.github/workflows/):

- **`ci.yml`**: Ejecuta lint, typecheck, tests y construcción Docker en cada Pull Request
- **Dependabot**: actualizaciones automáticas de Python, npm, Actions, Docker y Terraform

---

## Seguridad

Consulta [SECURITY.md](SECURITY.md) para conocer cómo reportar vulnerabilidades y la política de secretos.

**No incluyas nunca en el repositorio**: claves API, contraseñas, tokens JWT, certificados privados ni datos personales reales.

---

## Resolución de problemas

**El backend no arranca**
```bash
cd backend && uv sync
cat .env
```

**Error de migraciones**
```bash
cd backend && uv run alembic current && uv run alembic history
```

**El frontend no conecta con el backend**
- Verifica que `VITE_API_BASE_URL` apunta al puerto correcto
- Verifica que `CORS_ORIGINS` incluye la URL del frontend

---

## Roadmap

- [ ] Autenticación completa con múltiples usuarios
- [ ] Mapa interactivo de conciertos
- [ ] Integración con Setlist.fm
- [ ] Integración con Spotify para información de artistas
- [ ] Aplicación móvil (React Native)
- [ ] Notificaciones de aniversarios de conciertos
- [ ] Exportación a PDF

---

## Cómo contribuir

Lee [CONTRIBUTING.md](CONTRIBUTING.md) para conocer el proceso de contribución.

---

## Licencia

Este proyecto está bajo la licencia [MIT](LICENSE).

---

## Autoría

Creado por **falken20** – security@livememories.app

> Hecho con ❤️ para nunca olvidar ningún concierto.
