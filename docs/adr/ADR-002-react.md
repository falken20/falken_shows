# Architecture Decision Record – ADR-002

## Title: Choice of React as frontend framework

**Status**: Accepted  
**Date**: 2026-07-15  
**Context**: Live Memories

---

## Context

A frontend framework is needed for the single-page application. The main candidates were:

- **React** (with Vite)
- **Vue 3** (with Vite)
- **SvelteKit**

## Decision

Use **React 18** with **Vite** as the frontend stack.

## Rationale

- **Ecosystem maturity**: React has the largest ecosystem of UI libraries, data fetching tools, and state management solutions.
- **TypeScript support**: Excellent TypeScript support with mature type definitions.
- **Material UI**: MUI provides a comprehensive, accessible, and well-maintained component library.
- **TanStack Query**: The best-in-class data fetching and caching solution for React applications.
- **React Hook Form + Zod**: Battle-tested combination for form handling and validation.
- **Vite**: Extremely fast development server and optimised production builds.
- **Testing**: Vitest + React Testing Library provide an excellent testing experience.
- **i18next**: Mature internationalisation library with excellent React integration.

Vue 3 and SvelteKit were rejected primarily because the team has more React experience, and the MUI component library ecosystem is more mature for React.

## Consequences

- Functional components with hooks only; no class components.
- All server state must go through TanStack Query.
- All forms must use React Hook Form + Zod.
- Accessibility must be maintained through MUI components and custom ARIA where needed.
