terraform {
  required_version = ">= 1.9"

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 7.44"
    }
  }

  # Uncomment to use GCS remote state in production
  # backend "gcs" {
  #   bucket = "YOUR_STATE_BUCKET"
  #   prefix = "live-memories/terraform"
  # }
}
