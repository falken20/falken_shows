---
applyTo: "{backend/tests/**/*.py,frontend/src/**/*.test.{ts,tsx},frontend/e2e/**/*.ts}"
---

# Testing Instructions

## Backend tests (Pytest)

### Setup

- `asyncio_mode = "auto"` is set in `pyproject.toml` – no `@pytest.mark.asyncio` needed.
- Use the `db_session` fixture from `conftest.py` for a clean in-memory SQLite DB per test.
- Never use hardcoded IDs. Use builder/factory functions from `tests/factories.py`.

### Coverage requirements

- Minimum coverage: **80 %** (enforced with `--cov-fail-under=80`).
- Every endpoint must have:
  1. Happy path (200/201)
  2. Validation error (422)
  3. Not found (404) where applicable
  4. Auth required (401) for protected routes

### Structure

```
backend/tests/
├── conftest.py           # Fixtures: db_session, async_client, auth_headers
├── factories.py          # Test data builders
├── unit/
│   ├── test_<service>.py
│   └── test_<repository>.py
└── integration/
    └── test_<resource>.py
```

### Example integration test

```python
async def test_create_concert_happy_path(
    async_client: AsyncClient, auth_headers: dict[str, str]
) -> None:
    payload = build_concert_payload()
    response = await async_client.post("/api/v1/concerts", json=payload, headers=auth_headers)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == payload["title"]
```

## Frontend tests (Vitest + RTL)

- Test **user behaviour**, not implementation details.
- Avoid `getByTestId`. Prefer: `getByRole`, `getByLabelText`, `getByText`.
- Mock all API calls with **MSW** handlers in `src/mocks/handlers.ts`.
- Wrap components requiring providers with the shared `renderWithProviders` helper.

### Example component test

```tsx
it('displays concert title in the list', async () => {
  render(<ConcertList />, { wrapper: AppProviders });
  expect(await screen.findByText('Radiohead Live')).toBeInTheDocument();
});
```

## E2E tests (Playwright)

- Tests live in `frontend/e2e/`.
- Use the Page Object Model pattern.
- Test files named `<flow>.spec.ts`.
- Critical flows that must always be covered:
  1. Login
  2. Create concert
  3. Edit concert
  4. Search concert
  5. Delete concert

## Commands

```bash
make test-backend   # Pytest with coverage
make test-frontend  # Vitest
make test-e2e       # Playwright
```
