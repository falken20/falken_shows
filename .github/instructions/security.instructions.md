---
applyTo: "**/*.{py,ts,tsx}"
---

# Security Instructions

## Secrets

- **Never** commit `.env`, API keys, passwords, tokens, or certificates to the repository.
- Use `.env.example` for documentation only – no real values.
- In production, source secrets from **Google Secret Manager** via environment variables.
- Secrets must never appear in logs. Mask `password`, `token`, `secret` fields in log output.

## Input validation

- **Backend**: All inputs go through Pydantic v2 schemas. Add validators for sensitive fields.
- **Frontend**: All forms use Zod schemas validated by React Hook Form.
- Never trust client-side validation alone; always re-validate on the server.

## Authentication and authorisation

- Use JWT tokens with short expiry (`ACCESS_TOKEN_EXPIRE_MINUTES`).
- Hash passwords with **bcrypt** (via `passlib`). Never store plaintext passwords.
- Protected endpoints must require the `get_current_user` dependency.
- Return `401 Unauthorized` for missing/invalid auth; `403 Forbidden` for insufficient permissions.

## File uploads

- Validate MIME type using Pillow (`Image.open()`) – do not trust the `Content-Type` header alone.
- Enforce maximum file size before processing.
- Sanitise filenames: use UUIDs, not user-supplied names, for storage.
- Store files outside the web root (or in a private GCS bucket with signed URLs).

## HTTP security headers

Applied via middleware:
- `Strict-Transport-Security`
- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: DENY`
- `Content-Security-Policy`
- `Referrer-Policy: strict-origin-when-cross-origin`

## CORS

- Configure `CORS_ORIGINS` explicitly. Never use `*` in production.
- Backend reads allowed origins from `settings.CORS_ORIGINS`.

## SQL

- Use SQLAlchemy ORM or parameterised `text()` queries only.
- Never concatenate user input into SQL strings.

## Dependency hygiene

- Keep dependencies updated. Review Dependabot PRs promptly.
- Check new dependencies for known CVEs before adding them.

## Audit log

- Log all create, update, and delete operations with: timestamp, user ID, resource type, resource ID, action.
- Store audit logs separately; do not mix with application logs.
