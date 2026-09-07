# Servicios y recursos a gestionar

Este documento recoge los servicios de Google Cloud y otros recursos que probablemente necesitarás gestionar para mantener la aplicación Live Memories en funcionamiento.

## Google Cloud

### Aplicación y despliegue
- Cloud Run
  - Backend API
  - Frontend web
  - Revisión por entorno y tráfico
- Artifact Registry
  - Imágenes Docker del backend y frontend
  - Repositorios de imágenes
- Cloud Build
  - Compilación automática
  - Publicación de imágenes
  - Despliegue del backend y frontend

### Base de datos y almacenamiento
- Cloud SQL (PostgreSQL)
  - Base de datos principal
  - Backups y mantenimiento
  - Conexión privada
- Cloud Storage
  - Archivos estáticos
  - Búsquedas o almacenamiento de documentos adjuntos si se añade más funcionalidad
- Secret Manager
  - JWT
  - contraseña de base de datos
  - otros secretos de aplicación

### Seguridad y acceso
- IAM
  - roles y permisos de servicio
  - acceso a Cloud Run, Cloud SQL, Storage y Secret Manager
- Service Accounts
  - cuenta del backend
  - cuenta del frontend
  - cuenta de despliegue / CI
- Cloud Logging / Cloud Monitoring
  - logs de aplicación
  - métricas y alertas

### Red y networking
- VPC / private networking
  - acceso privado a Cloud SQL
  - control de tráfico entre servicios
- Load Balancer o rutas de acceso si se necesita exposición adicional

## Otros recursos del proyecto

- Repositorio GitHub
  - código del backend
  - código del frontend
  - pipelines CI/CD
- Docker / Docker Compose
  - entorno local
  - imágenes de contenedores
- Variables de entorno y configuración local
  - `.env`
  - configuración del proyecto
- Base de datos local para pruebas
  - PostgreSQL local o equivalente

## Gestión recomendada

Es recomendable mantener esta lista actualizada a medida que el proyecto crece. En general los elementos clave a vigilar son:

1. Cloud Run
2. Cloud SQL
3. Secret Manager
4. Artifact Registry
5. Cloud Storage
6. IAM y Service Accounts
7. Cloud Build
8. Logs y alertas

## Resumen rápido

Para empezar, lo mínimo habitual es gestionar:

- Cloud Run (backend + frontend)
- Cloud SQL (PostgreSQL)
- Secret Manager
- Artifact Registry
- Cloud Build
- IAM / Service Accounts
- Cloud Storage
- Logs y monitorización
