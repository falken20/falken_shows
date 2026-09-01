# Despliegue en GCP mediante consola

Esta guía describe la provisión mediante consola GCP. No elimina recursos existentes ni ejecuta operaciones destructivas.

## 1. Preparar el proyecto

1. En Google Cloud Console, selecciona o crea el proyecto.
2. Selecciona la región que usará Cloud Run, por ejemplo `europe-west1`.
3. En **APIs y servicios**, habilita Cloud Run, Cloud Build, Artifact Registry, Cloud SQL Admin, Secret Manager,
   Cloud Storage, IAM y Service Networking.
4. En **Facturación**, confirma que el proyecto tiene una cuenta activa.

## 2. Crear Artifact Registry

En **Artifact Registry > Repositories > Create repository**:

- Nombre: `live-memories`.
- Formato: Docker.
- Región: la misma que Cloud Run.
- Concede a la cuenta de servicio de Cloud Build el rol **Artifact Registry Writer**.

## 3. Crear secretos

En **Secret Manager > Create secret**, crea:

- `live-memories-jwt-secret`.
- `live-memories-db-password`.
- `live-memories-admin-password`.

Añade los valores únicamente desde la consola o desde un gestor seguro. No los guardes en el repositorio. Concede a la
cuenta de servicio del backend el rol **Secret Manager Secret Accessor** sobre cada secreto.

## 4. Crear Cloud SQL

En **Cloud SQL > Create instance > PostgreSQL**:

- Versión: PostgreSQL 16.
- Alta disponibilidad y tamaño según el entorno.
- Desactiva la IP pública.
- Configura IP privada y Private Service Access.
- Activa backups automáticos y protección contra eliminación.
- Exige conexiones TLS cuando el entorno lo permita.

Crea la base de datos `live_memories` y el usuario `live_memories`. Usa el valor de `live-memories-db-password` como
contraseña y no lo escribas en archivos de configuración.

## 5. Crear cuentas de servicio

Crea cuentas separadas para backend y frontend en **IAM y administración > Cuentas de servicio**.

Para el backend concede únicamente:

- **Cloud SQL Client**.
- **Secret Manager Secret Accessor** sobre los tres secretos.
- **Storage Object User** sobre el bucket de fotografías.

Para el frontend concede únicamente los roles necesarios para servir la imagen de Cloud Run.

## 6. Crear el bucket privado

En **Cloud Storage > Buckets > Create**:

- Usa la región elegida.
- Activa acceso uniforme a nivel de bucket.
- Activa prevención de acceso público.
- Configura ciclo de vida y retención según la política del proyecto.
- Concede **Storage Object User** únicamente al backend.

## 7. Crear el servicio backend

Primero publica una imagen del backend en Artifact Registry. Después, en **Cloud Run > Create service**:

- Servicio: `live-memories-backend`.
- Imagen: la imagen del backend publicada.
- Puerto: `8000`.
- Cuenta de servicio: la cuenta del backend.
- Configura el acceso público solo si se mantiene el diseño actual de lecturas públicas; los endpoints de escritura siguen
  requiriendo JWT.
- Añade las variables no sensibles del archivo `.env.example`.
- Añade como referencias de Secret Manager `JWT_SECRET_KEY`, `DB_PASSWORD` y `ADMIN_PASSWORD`.
- Configura `DATABASE_URL` con el socket `/cloudsql/PROJECT_ID:REGION:INSTANCE`.
- Añade la conexión de Cloud SQL en la sección **Connections**.
- Configura health checks para `/api/v1/health` y límites de CPU/memoria.

## 8. Crear el Job de migraciones

En **Cloud Run > Jobs > Create job**:

- Nombre: `live-memories-migrations`.
- Imagen: la misma imagen del backend.
- Comando: `alembic`.
- Argumentos: `upgrade head`.
- Cuenta de servicio: la cuenta del backend.
- Configura `DATABASE_URL`, `DB_PASSWORD` y la conexión de Cloud SQL igual que en el backend.
- Configura un máximo de un reintento.

Ejecuta el Job y verifica que termina correctamente antes de publicar una nueva revisión del backend.

## 9. Crear el servicio frontend

En **Cloud Run > Create service**:

- Servicio: `live-memories-frontend`.
- Imagen: la imagen frontend publicada.
- Puerto: `80`.
- Cuenta de servicio: la cuenta del frontend.
- Configura `/health` como health check.
- Permite acceso público para que los usuarios puedan abrir la aplicación.

La URL del backend debe estar incorporada durante el build mediante `VITE_API_BASE_URL`.

## 10. Configurar Cloud Build

En **Cloud Build > Triggers** crea un trigger para la rama `master` apuntando a
`infrastructure/cloudbuild/cloudbuild.yaml`. Configura las sustituciones:

- `_REGION`: región de Artifact Registry y Cloud Run.
- `_REPO`: `live-memories`.
- `_BACKEND_URL`: URL real del servicio backend.

La cuenta de servicio de Cloud Build necesita permisos para publicar en Artifact Registry, actualizar y ejecutar el Job de
migraciones y desplegar ambos servicios de Cloud Run.

## 11. Verificación y operación

Después del primer despliegue verifica en la consola:

- Revisión activa de ambos servicios.
- Ejecución exitosa del Job de migraciones.
- Logs sin secretos.
- Estado **Healthy** de Cloud Run y Cloud SQL.
- Acceso privado de Cloud SQL y del bucket.
- Permisos IAM sin `Editor` o `Owner` innecesarios.

Para rollback, selecciona una revisión anterior en Cloud Run. No borres la base de datos, el bucket ni los secretos como
parte de un rollback de aplicación.
