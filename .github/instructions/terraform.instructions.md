---
applyTo: "infrastructure/terraform/**/*.tf"
---

# Terraform Instructions

## General rules

- All resources use descriptive names: `live-memories-<environment>-<resource>`.
- Use variables for all environment-specific values; never hardcode project IDs, regions, or credentials.
- Use `terraform.tfvars` (gitignored) for actual values. Use `terraform.tfvars.example` for documentation.
- All modules must have `variables.tf`, `outputs.tf`, and `main.tf`.

## Security

- Service accounts follow least-privilege: grant only the roles explicitly needed.
- Never put secrets in `.tf` files. Reference them via `google_secret_manager_secret_version`.
- Enable audit logging for Cloud SQL and Secret Manager.
- Cloud Run services must run with a dedicated service account, not the default compute account.

## State management

- Use remote state (GCS backend) for all non-local environments.
- Lock state with `google_storage_bucket` versioning.

## Module structure

```
infrastructure/terraform/
├── main.tf           # Root module, calls sub-modules
├── variables.tf      # Input variables
├── outputs.tf        # Outputs
├── providers.tf      # Google provider config
├── versions.tf       # Required provider versions
├── terraform.tfvars.example
└── modules/
    ├── cloud-run/
    ├── cloud-sql/
    ├── storage/
    ├── artifact-registry/
    └── iam/
```

## Naming conventions

```
# Resource naming pattern:
"${var.project_id}-${var.environment}-live-memories-<resource_type>"
```

## Validation

```bash
cd infrastructure/terraform
terraform init
terraform validate
terraform fmt -check -recursive
```

Always run `terraform plan` and review output before `terraform apply`.
