# Indice de documentacion

Este documento es el punto de entrada para navegar por la documentacion de Live Memories.

## Ruta recomendada

Para una primera puesta en marcha, sigue este orden:

1. [README.md](../README.md): vision general, instalacion y comandos principales.
2. [LOCAL_TESTING.md](LOCAL_TESTING.md): configuracion y validacion local.
3. [API.md](API.md): endpoints y autenticacion de la API.
4. [SECURITY.md](../SECURITY.md): politica de seguridad y gestion de secretos.
5. [DEPLOYMENT_GCP_CONSOLE.md](DEPLOYMENT_GCP_CONSOLE.md): despliegue inicial en Google Cloud.
6. [SERVICES_AND_RESOURCES.md](SERVICES_AND_RESOURCES.md): inventario de recursos que hay que gestionar.

## Desarrollo y contribucion

| Documento | Utilidad | Estado |
|---|---|---|
| [CONTRIBUTING.md](../CONTRIBUTING.md) | Ramas, commits, tests, migraciones y pull requests. | Vigente |
| [LOCAL_TESTING.md](LOCAL_TESTING.md) | Instalacion, servidores locales, tests y Docker Compose. | Vigente |
| [TROUBLESHOOTING.md](TROUBLESHOOTING.md) | Diagnostico de problemas habituales. | Vigente |
| [API.md](API.md) | Referencia de endpoints actuales. | Vigente |
| [CHANGELOG.md](../CHANGELOG.md) | Historial de cambios del proyecto. | Vigente |

## Seguridad

| Documento | Utilidad | Estado |
|---|---|---|
| [SECURITY.md](../SECURITY.md) | Reporte de vulnerabilidades, secretos y controles de seguridad. | Vigente |
| [.env.example](../.env.example) | Plantilla de variables de entorno sin secretos reales. | Vigente |
| [docs/DEPLOYMENT_GCP_CONSOLE.md](DEPLOYMENT_GCP_CONSOLE.md) | Secret Manager, IAM, Cloud SQL y configuracion segura de Cloud Run. | Vigente, requiere valores del proyecto |

## Despliegue y operacion

| Documento | Utilidad | Estado |
|---|---|---|
| [DEPLOYMENT_GCP_CONSOLE.md](DEPLOYMENT_GCP_CONSOLE.md) | Provision inicial y despliegue manual en GCP. | Vigente |
| [SERVICES_AND_RESOURCES.md](SERVICES_AND_RESOURCES.md) | Cloud Run, Cloud SQL, Storage, IAM, Cloud Build y monitorizacion. | Vigente |
| [COST_ESTIMATE.md](COST_ESTIMATE.md) | Estimacion orientativa de costes. | Orientativo |
| [LOCAL_TESTING.md](LOCAL_TESTING.md) | Alternativa local con o sin Docker. | Vigente |

La automatizacion de Cloud Build se encuentra en [infrastructure/cloudbuild/cloudbuild.yaml](../infrastructure/cloudbuild/cloudbuild.yaml).
El workflow de validacion continua esta en [.github/workflows/ci.yml](../.github/workflows/ci.yml).

## Arquitectura y decisiones

| Documento | Utilidad | Estado |
|---|---|---|
| [ARCHITECTURE.md](../ARCHITECTURE.md) | Resumen de arquitectura y componentes principales. | Vigente |
| [docs/ARCHITECTURE.md](ARCHITECTURE.md) | Diagramas, flujos y arquitectura objetivo. | Vigente, incluye capacidades planificadas |
| [ADR-001-fastapi.md](adr/ADR-001-fastapi.md) | Decision sobre FastAPI. | Historico de decisiones |
| [ADR-002-react.md](adr/ADR-002-react.md) | Decision sobre React y Vite. | Vigente |
| [ADR-003-database.md](adr/ADR-003-database.md) | Decision sobre SQLite y PostgreSQL. | Vigente |
| [ADR-004-cloud-run.md](adr/ADR-004-cloud-run.md) | Decision sobre Cloud Run. | Vigente |
| [ADR-005-photo-storage.md](adr/ADR-005-photo-storage.md) | Propuesta para almacenamiento de fotos. | Propuesto, no implementado |
| [ADR-006-monorepo.md](adr/ADR-006-monorepo.md) | Decision sobre la estructura monorepo. | Vigente |

Los ADR explican decisiones tecnicas. No sustituyen las guias operativas de instalacion o despliegue.

## Documentacion de soporte del repositorio

Estos archivos contienen instrucciones para herramientas y colaboradores, no son guias de despliegue:

- [.github/copilot-instructions.md](../.github/copilot-instructions.md): contexto y convenciones para Copilot.
- [.github/instructions/](../.github/instructions/): reglas por area del proyecto.
- [.github/agents/](../.github/agents/): perfiles de agentes especializados.
- [.pre-commit-config.yaml](../.pre-commit-config.yaml): hooks de validacion local.
- [Makefile](../Makefile): comandos operativos disponibles.

## Fuente de verdad

Cuando exista una discrepancia, comprueba primero la implementacion actual:

- Dependencias: [backend/pyproject.toml](../backend/pyproject.toml) y [frontend/package.json](../frontend/package.json).
- API: routers en [backend/app/api/v1/endpoints](../backend/app/api/v1/endpoints) y [docs/API.md](API.md).
- Entorno local: [docker-compose.yml](../docker-compose.yml), [Makefile](../Makefile) y [.env.example](../.env.example).
- CI: [.github/workflows/ci.yml](../.github/workflows/ci.yml).
- Despliegue: [infrastructure/cloudbuild/cloudbuild.yaml](../infrastructure/cloudbuild/cloudbuild.yaml) y [DEPLOYMENT_GCP_CONSOLE.md](DEPLOYMENT_GCP_CONSOLE.md).

Las funcionalidades de fotografias, GCS, estadisticas, busqueda avanzada e importacion/exportacion estan planificadas y no forman parte de la API actual.
