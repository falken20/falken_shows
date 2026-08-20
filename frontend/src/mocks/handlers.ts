import { http, HttpResponse } from 'msw'

const API_BASE = 'http://localhost:8000/api/v1'

/**
 * MSW request handlers shared between Vitest (node) and browser dev mocking.
 *
 * Each handler intercepts a specific API route and returns a fixture response
 * so tests and storybook previews work without a running backend.
 *
 * To add a new handler for a new endpoint:
 * ```ts
 * http.get(`${API_BASE}/concerts`, () => HttpResponse.json([...]))
 * ```
 */
export const handlers = [
  http.get(`${API_BASE}/health`, () => {
    return HttpResponse.json({
      status: 'ok',
      app_name: 'Live Memories',
      version: '0.1.0',
      environment: 'testing',
    })
  }),

  http.get(`${API_BASE}/ready`, () => {
    return HttpResponse.json({
      status: 'ok',
      database: 'ok',
    })
  }),
]
