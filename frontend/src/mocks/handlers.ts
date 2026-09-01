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

  // Auth
  http.post(`${API_BASE}/auth/token`, () => {
    return HttpResponse.json({ access_token: 'mock-jwt-token', token_type: 'bearer' })
  }),

  // Artists
  http.get(`${API_BASE}/artists`, () => {
    return HttpResponse.json({
      items: [
        {
          id: 1,
          name: 'Mock Artist',
          bio: null,
          country: 'ES',
          created_at: '2024-01-01T00:00:00Z',
        },
      ],
      total: 1,
      page: 1,
      page_size: 20,
      pages: 1,
    })
  }),

  http.post(`${API_BASE}/artists`, async ({ request }) => {
    const body = (await request.json()) as Record<string, unknown>
    return HttpResponse.json(
      {
        id: 2,
        name: body.name,
        bio: body.bio ?? null,
        country: body.country ?? null,
        created_at: '2024-01-01T00:00:00Z',
      },
      { status: 201 }
    )
  }),

  http.put(`${API_BASE}/artists/:id`, async ({ params, request }) => {
    const body = (await request.json()) as Record<string, unknown>
    return HttpResponse.json({
      id: Number(params.id),
      name: body.name ?? 'Mock Artist',
      bio: null,
      country: 'ES',
      created_at: '2024-01-01T00:00:00Z',
    })
  }),

  http.delete(`${API_BASE}/artists/:id`, () => new HttpResponse(null, { status: 204 })),

  // Venues
  http.get(`${API_BASE}/venues`, () => {
    return HttpResponse.json({
      items: [
        {
          id: 1,
          name: 'Mock Venue',
          city: 'Madrid',
          country: 'ES',
          capacity: 500,
          created_at: '2024-01-01T00:00:00Z',
        },
      ],
      total: 1,
      page: 1,
      page_size: 20,
      pages: 1,
    })
  }),

  http.post(`${API_BASE}/venues`, async ({ request }) => {
    const body = (await request.json()) as Record<string, unknown>
    return HttpResponse.json(
      {
        id: 2,
        name: body.name,
        city: body.city,
        country: body.country,
        capacity: body.capacity ?? null,
        created_at: '2024-01-01T00:00:00Z',
      },
      { status: 201 }
    )
  }),

  http.put(`${API_BASE}/venues/:id`, async ({ params, request }) => {
    const body = (await request.json()) as Record<string, unknown>
    return HttpResponse.json({
      id: Number(params.id),
      name: body.name ?? 'Mock Venue',
      city: 'Madrid',
      country: 'ES',
      capacity: 500,
      created_at: '2024-01-01T00:00:00Z',
    })
  }),

  http.delete(`${API_BASE}/venues/:id`, () => new HttpResponse(null, { status: 204 })),

  // Concerts
  http.get(`${API_BASE}/concerts`, () => {
    return HttpResponse.json({
      items: [
        {
          id: 1,
          title: 'Mock Concert',
          artist: {
            id: 1,
            name: 'Mock Artist',
            bio: null,
            country: 'ES',
            created_at: '2024-01-01T00:00:00Z',
          },
          venue: {
            id: 1,
            name: 'Mock Venue',
            city: 'Madrid',
            country: 'ES',
            capacity: 500,
            created_at: '2024-01-01T00:00:00Z',
          },
          date: '2024-06-15T20:00:00Z',
          setlist: null,
          notes: null,
          rating: 4,
          ticket_price: 25.0,
          currency: 'EUR',
          created_at: '2024-01-01T00:00:00Z',
          updated_at: '2024-01-01T00:00:00Z',
        },
      ],
      total: 1,
      page: 1,
      page_size: 20,
      pages: 1,
    })
  }),

  http.get(`${API_BASE}/concerts/:id`, () => {
    return HttpResponse.json({
      id: 1,
      title: 'Mock Concert',
      artist: {
        id: 1,
        name: 'Mock Artist',
        bio: null,
        country: 'ES',
        created_at: '2024-01-01T00:00:00Z',
      },
      venue: {
        id: 1,
        name: 'Mock Venue',
        city: 'Madrid',
        country: 'ES',
        capacity: 500,
        created_at: '2024-01-01T00:00:00Z',
      },
      date: '2024-06-15T20:00:00Z',
      setlist: ['Song 1', 'Song 2'],
      notes: 'Great show',
      rating: 5,
      ticket_price: 30.0,
      currency: 'EUR',
      created_at: '2024-01-01T00:00:00Z',
      updated_at: '2024-01-01T00:00:00Z',
    })
  }),

  http.post(`${API_BASE}/concerts`, async ({ request }) => {
    const body = (await request.json()) as Record<string, unknown>
    return HttpResponse.json(
      {
        id: 2,
        title: body.title,
        artist: null,
        venue: null,
        date: body.date,
        setlist: null,
        notes: body.notes ?? null,
        rating: body.rating ?? null,
        ticket_price: body.ticket_price ?? null,
        currency: body.currency ?? 'EUR',
        created_at: '2024-01-01T00:00:00Z',
        updated_at: '2024-01-01T00:00:00Z',
      },
      { status: 201 }
    )
  }),

  http.put(`${API_BASE}/concerts/:id`, async ({ params, request }) => {
    const body = (await request.json()) as Record<string, unknown>
    return HttpResponse.json({
      id: Number(params.id),
      title: body.title ?? 'Mock Concert',
      artist: null,
      venue: null,
      date: body.date ?? '2024-06-15T20:00:00Z',
      setlist: null,
      notes: body.notes ?? null,
      rating: body.rating ?? null,
      ticket_price: body.ticket_price ?? null,
      currency: body.currency ?? 'EUR',
      created_at: '2024-01-01T00:00:00Z',
      updated_at: '2024-01-01T00:00:00Z',
    })
  }),

  http.delete(`${API_BASE}/concerts/:id`, () => new HttpResponse(null, { status: 204 })),
]
