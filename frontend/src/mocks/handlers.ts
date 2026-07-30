import { http, HttpResponse } from 'msw'

const API_BASE = 'http://localhost:8000/api/v1'

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
