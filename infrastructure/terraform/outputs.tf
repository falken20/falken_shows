output "backend_url" {
  description = "Cloud Run backend service URL"
  value       = google_cloud_run_v2_service.backend.uri
}

output "frontend_url" {
  description = "Cloud Run frontend service URL"
  value       = google_cloud_run_v2_service.frontend.uri
}

output "artifact_registry_url" {
  description = "Artifact Registry repository URL"
  value       = "${var.region}-docker.pkg.dev/${var.project_id}/${google_artifact_registry_repository.live_memories.repository_id}"
}

output "cloud_sql_connection_name" {
  description = "Cloud SQL connection name for the backend"
  value       = google_sql_database_instance.main.connection_name
}

output "uploads_bucket_name" {
  description = "GCS bucket name for file uploads"
  value       = google_storage_bucket.uploads.name
}

output "backend_service_account" {
  description = "Backend service account email"
  value       = google_service_account.backend.email
}
