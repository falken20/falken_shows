# Troubleshooting

Common issues and solutions for the Live Memories development environment.

---

## Backend

### `ModuleNotFoundError` when running tests

**Symptom:** `ImportError: No module named 'app'`

**Cause:** Tests must be run from inside the `backend/` directory or via the Makefile targets.

```bash
# Correct
cd backend && uv run pytest

# Or from the root
make test-backend
```

---

### Database migration errors

**Symptom:** `sqlalchemy.exc.OperationalError: no such table: concerts`

**Cause:** Tables have not been created. In development, the app creates them automatically on startup; in production, Alembic manages migrations.

```bash
# Apply all pending migrations
cd backend && uv run alembic upgrade head

# Check current migration state
cd backend && uv run alembic current
```

---

### `ValidationError` on startup for `JWT_SECRET_KEY`

**Symptom:**
```
pydantic_core._pydantic_core.ValidationError:
  JWT_SECRET_KEY must be at least 32 characters in production
```

**Cause:** `APP_ENV=production` requires a strong secret key.

**Fix:** Set a 32+ character random string in your `.env` file:
```bash
# Generate a strong key
python -c "import secrets; print(secrets.token_hex(32))"
```

Then update `.env`:
```
JWT_SECRET_KEY=<generated-key>
APP_ENV=development  # or production with a strong key
```

---

### CORS errors in browser console

**Symptom:** `Access to XMLHttpRequest blocked by CORS policy`

**Cause:** The frontend origin is not in `CORS_ORIGINS`.

**Fix:** Add your frontend URL to `.env`:
```
CORS_ORIGINS=http://localhost:5173,http://localhost:4173
```

---

### Port already in use

**Symptom:** `OSError: [Errno 48] Address already in use`

```bash
# Find and kill the process using port 8000
lsof -ti:8000 | xargs kill -9
# Or for port 5173 (frontend)
lsof -ti:5173 | xargs kill -9
```

---

### `aiosqlite` / async database errors in tests

**Symptom:** `RuntimeError: no running event loop` or session errors

**Cause:** Tests must use the async fixtures from `conftest.py`. Ensure you are not mixing sync and async calls.

```python
# Correct usage in tests
async def test_example(async_client: AsyncClient, db_session: AsyncSession) -> None:
    ...
```

---

### Passlib deprecation warning (`crypt` module)

**Symptom:**
```
DeprecationWarning: 'crypt' is deprecated and slated for removal in Python 3.13
```

**Cause:** `passlib[bcrypt]` uses Python's `crypt` module on some platforms. This is a known upstream issue. It does not affect functionality.

**Workaround:** Suppress the warning in `pyproject.toml` or upgrade to `passlib>=1.7.5` when available.

---

## Frontend

### `VITE_API_BASE_URL` not being picked up

**Symptom:** API calls go to the wrong URL.

**Cause:** Vite only exposes variables prefixed with `VITE_`. Check that your `.env` file is in `frontend/` and the variable is set.

```bash
# frontend/.env (create if missing)
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

---

### `Cannot find module '@/...'` TypeScript errors

**Symptom:** TypeScript cannot resolve `@/` path aliases.

**Cause:** The `tsconfig.json` path alias must match the `vite.config.ts` alias.

Check `frontend/tsconfig.json`:
```json
{
  "compilerOptions": {
    "paths": {
      "@/*": ["./src/*"]
    }
  }
}
```

And `frontend/vite.config.ts`:
```ts
resolve: {
  alias: { '@': '/src' }
}
```

---

### MSW (Mock Service Worker) not intercepting requests in tests

**Symptom:** Tests make real HTTP calls instead of using mock handlers.

**Cause:** The MSW server is not set up in test configuration.

**Fix:** Ensure `frontend/src/test/setup.ts` (or the equivalent) starts the server:
```ts
import { server } from '@/mocks/server'
beforeAll(() => server.listen())
afterEach(() => server.resetHandlers())
afterAll(() => server.close())
```

---

### Frontend build fails with `out of memory`

**Symptom:** `FATAL ERROR: CALL_AND_RETRY_LAST Allocation failed - JavaScript heap out of memory`

**Fix:**
```bash
NODE_OPTIONS=--max_old_space_size=4096 npm run build
```

---

## Docker / Infrastructure

### Docker Compose not starting services

**Symptom:** Services fail to start with networking errors.

```bash
# Check Docker daemon is running
docker info

# Remove stale containers and volumes
docker compose down -v
docker compose up --build
```

---

### Cloud Run service returns 403

**Symptom:** `403 Forbidden` from Cloud Run URL.

**Cause:** The service requires an authenticated invoker (Google identity). The frontend service account must have the `roles/run.invoker` role on the backend service.

**Fix:** Check the Terraform IAM binding in `infrastructure/terraform/iam.tf`.

---

### Alembic `Target database is not up to date`

**Symptom:** `alembic.util.exc.CommandError: Target database is not up to date.`

```bash
cd backend
uv run alembic upgrade head
```

---

## Common `make` Commands

| Command | Description |
|---------|-------------|
| `make install` | Install all dependencies |
| `make dev` | Start both backend and frontend in dev mode |
| `make test` | Run all tests |
| `make lint` | Run all linters |
| `make format` | Auto-format all code |
| `make typecheck` | Run Mypy + TypeScript type checks |
| `make migrate` | Apply pending Alembic migrations |
| `make migrate-create MSG="..."` | Create a new migration file |
