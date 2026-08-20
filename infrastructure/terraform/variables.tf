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

variable "vpc_network_id" {
  description = "VPC network self_link for Cloud SQL private IP"
  type        = string
}

variable "jwt_secret_version" {
  description = "Secret Manager version for JWT secret"
  type        = string
  default     = "latest"
}

variable "db_password_secret_version" {
  description = "Secret Manager version for DB password"
  type        = string
  default     = "latest"
}

variable "admin_password_secret_version" {
  description = "Secret Manager version for admin password"
  type        = string
  default     = "latest"
}
