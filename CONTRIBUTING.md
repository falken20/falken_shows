# Contributing to Live Memories

Thank you for your interest in contributing! This document explains how to set up your environment, create branches, write commits, and submit pull requests.

---

## Preparing your environment

```bash
git clone https://github.com/[YOUR_GITHUB_USER]/live-memories.git
cd live-memories
cp .env.example .env
make install
make pre-commit-install
make migrate
```

Verify everything works:

```bash
make test
make lint
make typecheck
```

---

## Branch naming convention

```
feat/short-description
fix/issue-number-short-description
chore/description
docs/description
refactor/description
test/description
```

Examples:

```
feat/add-setlist-endpoint
fix/42-duplicate-concert-detection
docs/update-deployment-guide
```

**Never push directly to `main` or `master`.**

---

## Commit convention

This project follows [Conventional Commits](https://www.conventionalcommits.org/).

```
<type>(<scope>): <short description>

[optional body]

[optional footer(s)]
```

Allowed types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`, `ci`, `build`, `revert`

Examples:

```
feat(concerts): add duplicate detection on create
fix(auth): handle expired JWT gracefully
test(venues): add integration tests for venue endpoints
chore(deps): update fastapi to 0.115
```

The pre-commit hook will enforce this format on `commit-msg`.

---

## Pull requests

1. Fork the repo and create your branch from `master`.
2. Make sure all tests pass: `make test`
3. Make sure linting and type checking pass: `make lint && make typecheck`
4. Add or update tests for every new feature or bug fix.
5. Update documentation and `CHANGELOG.md` if needed.
6. Open a PR with a clear title following Conventional Commits.
7. Fill in the PR template.
8. Request a review from a maintainer.

---

## Required tests

- **Backend**: All new endpoints must have integration tests. All new services/repositories must have unit tests. Coverage must remain ≥ 80 %.
- **Frontend**: New components must have unit tests. New pages with forms must have form interaction tests.
- **E2E**: Major user flows must be covered by Playwright tests.

---

## Code quality checks

Before opening a PR, run:

```bash
make format      # Auto-format code
make lint        # Fix linting issues
make typecheck   # Ensure no type errors
make test        # Ensure all tests pass
```

The CI pipeline will fail if any of these checks do not pass.

---

## Database migrations

When you modify a SQLAlchemy model:

```bash
make migrate-create MSG="describe the change"
# Review the generated file in backend/alembic/versions/
make migrate
```

Rules:
- Always review auto-generated migrations before committing.
- Migrations must work with both SQLite and PostgreSQL unless documented otherwise.
- Never edit a migration that has already been applied in production.
- Include both `upgrade()` and `downgrade()` functions.

---

## Adding dependencies

**Backend (Python)**:
```bash
cd backend
uv add package-name
# or for dev dependencies:
uv add --dev package-name
```

**Frontend (Node)**:
```bash
cd frontend
npm install package-name
# or for dev dependencies:
npm install --save-dev package-name
```

Rules:
- Justify the addition in the PR description.
- Prefer libraries that are actively maintained and have a permissive license.
- Avoid adding dependencies that duplicate existing functionality.
- Keep transitive dependencies in mind (bundle size for frontend, security for backend).

---

## Documentation

- Update `README.md` if you change setup steps, commands, or architecture.
- Add an ADR in `docs/adr/` for significant architectural decisions.
- Keep inline comments minimal and meaningful.

---

## Code of conduct

Please read and follow our [Code of Conduct](CODE_OF_CONDUCT.md).
