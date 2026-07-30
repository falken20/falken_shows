# Security Policy

## Reporting a vulnerability

If you discover a security vulnerability in Live Memories, **please do not open a public GitHub issue**.

Instead, report it privately by emailing: **[YOUR SECURITY EMAIL]**

Include in your report:

- A clear description of the vulnerability.
- Steps to reproduce it.
- The potential impact (data exposure, authentication bypass, etc.).
- Any proof-of-concept code or screenshots (if applicable).
- Suggested fix (optional).

We will acknowledge your report within **72 hours** and aim to release a fix within **14 days** for critical vulnerabilities.

---

## What NOT to include in public channels

- Credentials, tokens, or API keys.
- Personal data belonging to other users.
- Details that could be exploited before a fix is released.

---

## Supported versions

| Version | Supported |
|---|---|
| Latest `master` | ✅ Yes |
| Older releases | ❌ No |

Only the latest version receives security updates.

---

## Secrets management best practices

- Never commit `.env` files or any file containing real credentials.
- Use `.env.example` as a template – it must never contain real values.
- In production, use **Google Secret Manager** or equivalent.
- Rotate secrets immediately if you suspect they have been compromised.
- JWT secret keys must be long (≥ 32 random characters) and unique per environment.
- Database passwords must be strong and different across environments.
- Docker images must not contain secrets baked in – use runtime environment variables or Secret Manager.

---

## Known security controls

- JWT-based authentication with configurable expiry.
- Bcrypt password hashing.
- Strict Pydantic input validation on all endpoints.
- CORS restricted to configured origins.
- File upload validation (type, size) with Pillow verification.
- Security headers (HSTS, X-Frame-Options, X-Content-Type-Options) via middleware.
- No sensitive data in logs (passwords, tokens are masked).
- Audit log for create, update, and delete operations.
