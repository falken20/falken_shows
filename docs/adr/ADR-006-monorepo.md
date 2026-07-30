# Architecture Decision Record – ADR-006

## Title: Monorepo structure

**Status**: Accepted  
**Date**: 2026-07-15  
**Context**: Live Memories

---

## Context

The project has two main components: a FastAPI backend and a React frontend, plus shared infrastructure code. The options were:

- **Monorepo**: Single repository containing all components.
- **Polyrepo**: Separate repositories for frontend, backend, and infrastructure.

## Decision

Use a **monorepo** structure with a single Git repository.

## Rationale

- **Atomic changes**: Frontend and backend API changes can be committed together, keeping them in sync.
- **Simplified CI/CD**: A single CI pipeline manages both components, with path-based conditionals to skip unchanged parts.
- **Discoverability**: All code, documentation, and infrastructure is in one place.
- **Reduced overhead**: No need to manage multiple repositories, GitHub Actions secrets, or Dependabot configurations.
- **Project size**: This is a personal project with a single team (one developer), where monorepo coordination overhead is negligible.

Polyrepo was rejected because the synchronisation overhead between repos outweighs the benefits for a project of this size.

## Consequences

- Both frontend and backend use the same Git history.
- CI runs the full test suite but can skip frontend/backend jobs based on changed paths.
- Dependabot is configured separately for Python, npm, and GitHub Actions within the same repository.
- The `Makefile` provides unified commands that operate on the correct subdirectory.

## Directory structure

```
live-memories/
├── backend/     # Python/FastAPI API
├── frontend/    # React/TypeScript SPA
├── infrastructure/  # Terraform + Cloud Build
├── docs/        # Documentation and ADRs
└── scripts/     # Utility scripts
```
