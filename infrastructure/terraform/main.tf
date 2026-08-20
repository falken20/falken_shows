locals {
  resource_prefix = "${var.project_id}-${var.environment}-${var.app_name}"
  common_labels = {
    app         = var.app_name
    environment = var.environment
    managed_by  = "terraform"
  }
}

# ── Enable required APIs ──────────────────────────────────────
resource "google_project_service" "apis" {
  for_each = toset([
    "run.googleapis.com",
    "sqladmin.googleapis.com",
    "storage.googleapis.com",
    "artifactregistry.googleapis.com",
    "secretmanager.googleapis.com",
    "cloudbuild.googleapis.com",
    "iam.googleapis.com",
  ])

  project            = var.project_id
  service            = each.value
  disable_on_destroy = false
}

# ── Artifact Registry ─────────────────────────────────────────
resource "google_artifact_registry_repository" "live_memories" {
  project       = var.project_id
  location      = var.region
  repository_id = var.app_name
  description   = "Docker images for Live Memories"
  format        = "DOCKER"
  labels        = local.common_labels

  depends_on = [google_project_service.apis]
}

# ── Service Accounts ──────────────────────────────────────────
resource "google_service_account" "backend" {
  project      = var.project_id
  account_id   = "${var.app_name}-backend"
  display_name = "Live Memories Backend Service Account"
}

resource "google_service_account" "frontend" {
  project      = var.project_id
  account_id   = "${var.app_name}-frontend"
  display_name = "Live Memories Frontend Service Account"
}

# ── Cloud SQL ─────────────────────────────────────────────────
resource "google_sql_database_instance" "main" {
  project          = var.project_id
  name             = "${local.resource_prefix}-db"
  database_version = "POSTGRES_16"
  region           = var.region

  settings {
    tier = var.db_instance_tier

    database_flags {
      name  = "max_connections"
      value = "100"
    }

    backup_configuration {
      enabled    = true
      start_time = "03:00"
    }

    ip_configuration {
      ipv4_enabled    = false
      private_network = var.vpc_network_id
      ssl_mode        = "ENCRYPTED_ONLY"
    }
  }

  deletion_protection = true

  depends_on = [google_project_service.apis]
}

resource "google_sql_database" "live_memories" {
  project  = var.project_id
  name     = var.db_name
  instance = google_sql_database_instance.main.name
}

resource "google_sql_user" "app" {
  project  = var.project_id
  name     = var.db_user
  instance = google_sql_database_instance.main.name
  password = data.google_secret_manager_secret_version.db_password.secret_data
}

# Grant backend SA Cloud SQL Client role
resource "google_project_iam_member" "backend_cloudsql" {
  project = var.project_id
  role    = "roles/cloudsql.client"
  member  = "serviceAccount:${google_service_account.backend.email}"
}

# ── Secret Manager ────────────────────────────────────────────
data "google_secret_manager_secret_version" "db_password" {
  project = var.project_id
  secret  = "live-memories-db-password"
  version = var.db_password_secret_version
}

# Grant backend SA access to secrets
resource "google_secret_manager_secret_iam_member" "backend_jwt" {
  project   = var.project_id
  secret_id = "live-memories-jwt-secret"
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${google_service_account.backend.email}"
}

resource "google_secret_manager_secret_iam_member" "backend_db_password" {
  project   = var.project_id
  secret_id = "live-memories-db-password"
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${google_service_account.backend.email}"
}

resource "google_secret_manager_secret_iam_member" "backend_admin_password" {
  project   = var.project_id
  secret_id = "live-memories-admin-password"
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${google_service_account.backend.email}"
}

# ── Cloud Storage ─────────────────────────────────────────────
resource "google_storage_bucket" "uploads" {
  project       = var.project_id
  name          = "${local.resource_prefix}-uploads"
  location      = var.region
  force_destroy = false
  labels        = local.common_labels

  uniform_bucket_level_access = true

  lifecycle_rule {
    condition {
      age = 365
    }
    action {
      type          = "SetStorageClass"
      storage_class = "NEARLINE"
    }
  }
}

resource "google_storage_bucket_iam_member" "backend_storage" {
  bucket = google_storage_bucket.uploads.name
  role   = "roles/storage.objectAdmin"
  member = "serviceAccount:${google_service_account.backend.email}"
}

# ── Cloud Run – Backend ───────────────────────────────────────
resource "google_cloud_run_v2_service" "backend" {
  project  = var.project_id
  name     = "${var.app_name}-backend"
  location = var.region
  labels   = local.common_labels

  template {
    service_account = google_service_account.backend.email

    containers {
      image = var.backend_image

      ports {
        container_port = 8000
      }

      env {
        name  = "APP_ENV"
        value = var.environment
      }

      env {
        name  = "DATABASE_URL"
        value = "postgresql+psycopg2://${var.db_user}@/${var.db_name}?host=/cloudsql/${google_sql_database_instance.main.connection_name}"
      }

      env {
        name = "DB_PASSWORD"
        value_source {
          secret_key_ref {
            secret  = "live-memories-db-password"
            version = var.db_password_secret_version
          }
        }
      }

      env {
        name = "JWT_SECRET_KEY"
        value_source {
          secret_key_ref {
            secret  = "live-memories-jwt-secret"
            version = var.jwt_secret_version
          }
        }
      }

      env {
        name = "ADMIN_PASSWORD"
        value_source {
          secret_key_ref {
            secret  = "live-memories-admin-password"
            version = var.admin_password_secret_version
          }
        }
      }

      env {
        name  = "STORAGE_BACKEND"
        value = "gcs"
      }

      env {
        name  = "GCS_BUCKET_NAME"
        value = google_storage_bucket.uploads.name
      }

      env {
        name  = "GCP_PROJECT_ID"
        value = var.project_id
      }

      resources {
        limits = {
          cpu    = "1"
          memory = "512Mi"
        }
      }

      startup_probe {
        http_get {
          path = "/api/v1/health"
        }
        initial_delay_seconds = 10
        period_seconds        = 5
        failure_threshold     = 3
      }

      liveness_probe {
        http_get {
          path = "/api/v1/health"
        }
        period_seconds    = 30
        failure_threshold = 3
      }
    }

    volumes {
      name = "cloudsql"
      cloud_sql_instance {
        instances = [google_sql_database_instance.main.connection_name]
      }
    }

    scaling {
      min_instance_count = 0
      max_instance_count = 3
    }
  }

  depends_on = [google_project_service.apis]
}

# Backend requires authentication – invoked only via frontend proxy or authenticated clients
resource "google_cloud_run_v2_service_iam_member" "backend_invoker" {
  project  = var.project_id
  location = var.region
  name     = google_cloud_run_v2_service.backend.name
  role     = "roles/run.invoker"
  member   = "serviceAccount:${google_service_account.frontend.email}"
}

# ── Cloud Run – Frontend ──────────────────────────────────────
resource "google_cloud_run_v2_service" "frontend" {
  project  = var.project_id
  name     = "${var.app_name}-frontend"
  location = var.region
  labels   = local.common_labels

  template {
    service_account = google_service_account.frontend.email

    containers {
      image = var.frontend_image

      ports {
        container_port = 80
      }

      resources {
        limits = {
          cpu    = "0.5"
          memory = "256Mi"
        }
      }

      startup_probe {
        http_get {
          path = "/health"
        }
        initial_delay_seconds = 5
        period_seconds        = 5
        failure_threshold     = 3
      }
    }

    scaling {
      min_instance_count = 0
      max_instance_count = 3
    }
  }

  depends_on = [google_project_service.apis]
}

resource "google_cloud_run_v2_service_iam_member" "frontend_public" {
  project  = var.project_id
  location = var.region
  name     = google_cloud_run_v2_service.frontend.name
  role     = "roles/run.invoker"
  member   = "allUsers"
}
