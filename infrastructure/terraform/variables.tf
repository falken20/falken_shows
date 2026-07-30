variable "project_id" {
  description = "GCP Project ID"
  type        = string
}

variable "region" {
  description = "GCP region for resources"
  type        = string
  default     = "europe-west1"
}

variable "environment" {
  description = "Deployment environment (production, staging)"
  type        = string
  default     = "production"

  validation {
    condition     = contains(["production", "staging"], var.environment)
    error_message = "Environment must be 'production' or 'staging'."
  }
}

variable "app_name" {
  description = "Application name used for resource naming"
  type        = string
  default     = "live-memories"
}

variable "backend_image" {
  description = "Full Docker image URL for the backend service"
  type        = string
}

variable "frontend_image" {
  description = "Full Docker image URL for the frontend service"
  type        = string
}

variable "db_instance_tier" {
  description = "Cloud SQL instance tier"
  type        = string
  default     = "db-f1-micro"
}

variable "db_name" {
  description = "Cloud SQL database name"
  type        = string
  default     = "live_memories"
}

variable "db_user" {
  description = "Cloud SQL database user"
  type        = string
  default     = "live_memories"
}
