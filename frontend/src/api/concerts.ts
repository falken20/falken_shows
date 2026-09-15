import { apiClient } from './client'
import type {
  ArtistCreate,
  ArtistResponse,
  ArtistUpdate,
  ConcertCreate,
  ConcertResponse,
  ConcertUpdate,
  PaginatedResponse,
  TokenResponse,
  VenueCreate,
  VenueResponse,
  VenueUpdate,
} from '@/types'

/** Auth endpoints */
export const authApi = {
  login: (username: string, password: string): Promise<TokenResponse> => {
    const params = new URLSearchParams()
    params.append('username', username)
    params.append('password', password)
    return apiClient
      .post<TokenResponse>('/auth/token', params, {
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      })
      .then(r => r.data)
  },
  logout: (): Promise<void> => apiClient.post('/auth/logout').then(() => undefined),
}

/** Artist CRUD endpoints (token attached by Axios interceptor) */
export const artistsApi = {
  getAll: (page = 1, pageSize = 20): Promise<PaginatedResponse<ArtistResponse>> =>
    apiClient
      .get<PaginatedResponse<ArtistResponse>>('/artists', {
        params: { page, page_size: pageSize },
      })
      .then(r => r.data),

  getById: (id: number): Promise<ArtistResponse> =>
    apiClient.get<ArtistResponse>(`/artists/${id}`).then(r => r.data),

  create: (data: ArtistCreate): Promise<ArtistResponse> =>
    apiClient.post<ArtistResponse>('/artists', data).then(r => r.data),

  update: (id: number, data: ArtistUpdate): Promise<ArtistResponse> =>
    apiClient.put<ArtistResponse>(`/artists/${id}`, data).then(r => r.data),

  delete: (id: number): Promise<void> => apiClient.delete(`/artists/${id}`).then(() => undefined),
}

/** Venue CRUD endpoints */
export const venuesApi = {
  getAll: (page = 1, pageSize = 20): Promise<PaginatedResponse<VenueResponse>> =>
    apiClient
      .get<PaginatedResponse<VenueResponse>>('/venues', {
        params: { page, page_size: pageSize },
      })
      .then(r => r.data),

  getById: (id: number): Promise<VenueResponse> =>
    apiClient.get<VenueResponse>(`/venues/${id}`).then(r => r.data),

  create: (data: VenueCreate): Promise<VenueResponse> =>
    apiClient.post<VenueResponse>('/venues', data).then(r => r.data),

  update: (id: number, data: VenueUpdate): Promise<VenueResponse> =>
    apiClient.put<VenueResponse>(`/venues/${id}`, data).then(r => r.data),

  delete: (id: number): Promise<void> => apiClient.delete(`/venues/${id}`).then(() => undefined),
}

/** Concert CRUD endpoints */
export const concertsApi = {
  getAll: (page = 1, pageSize = 20): Promise<PaginatedResponse<ConcertResponse>> =>
    apiClient
      .get<PaginatedResponse<ConcertResponse>>('/concerts', {
        params: { page, page_size: pageSize },
      })
      .then(r => r.data),

  getById: (id: number): Promise<ConcertResponse> =>
    apiClient.get<ConcertResponse>(`/concerts/${id}`).then(r => r.data),

  create: (data: ConcertCreate): Promise<ConcertResponse> =>
    apiClient.post<ConcertResponse>('/concerts', data).then(r => r.data),

  update: (id: number, data: ConcertUpdate): Promise<ConcertResponse> =>
    apiClient.put<ConcertResponse>(`/concerts/${id}`, data).then(r => r.data),

  delete: (id: number): Promise<void> => apiClient.delete(`/concerts/${id}`).then(() => undefined),
}
