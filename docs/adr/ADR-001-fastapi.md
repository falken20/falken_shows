# Architecture Decision Record – ADR-001

## Title: Choice of FastAPI as backend framework

**Status**: Accepted  
**Date**: 2026-07-15  
**Context**: Live Memories

---

## Context

A backend framework is needed for the REST API. The main candidates were:

- **FastAPI** (Python)
- **Django REST Framework** (Python)
- **Flask** (Python)

The application is a personal project expected to have moderate complexity, with asynchronous I/O, auto-generated OpenAPI documentation, and a need for strong type validation.

## Decision

Use **FastAPI** as the backend framework.

## Rationale

- **Performance**: FastAPI is one of the fastest Python frameworks, suitable for async I/O.
- **OpenAPI out of the box**: Swagger UI and ReDoc are automatically generated from route definitions.
- **Pydantic integration**: Request/response validation through Pydantic v2 schemas with zero boilerplate.
- **Type safety**: First-class support for Python type hints, enabling Mypy strict mode.
- **Dependency injection**: Clean `Depends()` system for authentication, DB sessions, and other shared dependencies.
- **Async support**: Native `async/await` for database access and external API calls.
- **Ecosystem**: Well-maintained, growing community, excellent documentation.

Django REST Framework was rejected due to its higher overhead and ORM coupling. Flask was rejected due to the need for more boilerplate.

## Consequences

- All endpoints must use async handler functions or run synchronous code in a thread pool.
- Pydantic v2 schemas are required for all request/response models.
- OpenAPI documentation is automatically maintained alongside the code.
- The application can easily add WebSocket support in the future.
