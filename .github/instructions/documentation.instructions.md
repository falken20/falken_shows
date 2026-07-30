---
applyTo: "docs/**/*.md"
---

# Documentation Instructions

## Docstrings

- Add docstrings only to **public** functions and classes where the purpose is not obvious.
- Use Google-style docstrings in Python.
- Avoid restating what the type annotations already say.

## Comments

- Comments explain **why**, not **what**.
- Remove commented-out code before merging.
- TODO comments must reference an issue number: `# TODO(#42): implement rate limiting`.

## README

- Keep installation instructions accurate and tested.
- Every new major feature needs a section in README.
- Command examples must be copy-pasteable and work on macOS/Linux.

## CHANGELOG

- Follow [Keep a Changelog](https://keepachangelog.com) format.
- Every PR that changes user-visible behaviour must include a CHANGELOG entry.
- Categories: `Added`, `Changed`, `Deprecated`, `Removed`, `Fixed`, `Security`.

## ADRs (Architectural Decision Records)

- File: `docs/adr/ADR-NNN-short-title.md`
- Template sections: `Status`, `Context`, `Decision`, `Consequences`.
- Create an ADR for any significant architectural decision.
- Status values: `Proposed`, `Accepted`, `Deprecated`, `Superseded by ADR-NNN`.

## API documentation

- All endpoints must have OpenAPI `summary`, `description`, and example responses.
- Use Pydantic `model_config` with `json_schema_extra` for request/response examples.
- Keep Swagger UI accessible at `/docs` and ReDoc at `/redoc`.
