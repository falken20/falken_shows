---
applyTo: "frontend/**/*.{ts,tsx}"
---

# Frontend React/TypeScript Instructions

## Component rules

- Functional components only. No class components.
- One component per file. File name = component name (PascalCase).
- Export structure:
  ```
  src/components/<Category>/<ComponentName>.tsx
  src/components/<Category>/<ComponentName>.test.tsx
  src/components/<Category>/index.ts  ← named export
  ```

## TypeScript

- Strict mode. No `any` without a comment explaining why.
- Define shared types in `src/types/`.
- Avoid `as` type assertions unless unavoidable (and comment why).

## State and data fetching

- Use **TanStack Query** for all server state.
- Never use raw `fetch` or `axios` directly inside components.
- All API calls go through `src/api/` modules.
- Example:
  ```ts
  // src/api/concerts.ts
  export const getConcerts = (params: ConcertListParams) =>
    apiClient.get<PaginatedResponse<Concert>>('/concerts', { params });
  ```

## Forms

- Use **React Hook Form** + **Zod** for all forms.
- Never rely on uncontrolled form state for complex forms.
- Display inline field errors below each input.

## Routing

- Use **React Router v6**.
- Type route params: `useParams<{ concertId: string }>()`.
- Use `useNavigate` for programmatic navigation.

## Internationalisation

- Use `i18next` / `react-i18next` for all user-facing strings.
- **Never hardcode** user-visible strings.
- Translation keys go in `src/i18n/locales/es.json` and `en.json`.

## Accessibility

- All interactive elements must be keyboard-accessible.
- Form inputs must have associated `<label>` elements.
- Images must have meaningful `alt` text (or `alt=""` if decorative).
- Use ARIA attributes only when native HTML semantics are insufficient.
- Maintain WCAG 2.1 AA colour contrast ratios.

## Styling

- Use **Material UI** components.
- Extend with `sx` prop or `styled()`. Avoid inline `style={{}}`.
- Support dark and light mode via MUI `ThemeProvider`.

## Commands

```bash
cd frontend
npm run lint       # ESLint
npm run format     # Prettier
npm run typecheck  # tsc --noEmit
npm run test:run   # Vitest
```
