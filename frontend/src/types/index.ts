/** Token response from POST /auth/token */
export interface TokenResponse {
  access_token: string
  token_type: string
}

/** Request body for login */
export interface LoginRequest {
  username: string
  password: string
}

/** Artist as returned by the API */
export interface ArtistResponse {
  id: number
  name: string
  bio: string | null
  country: string | null
  created_at: string
}

/** Payload for creating an artist */
export interface ArtistCreate {
  name: string
  bio?: string | null
  country?: string | null
}

/** Payload for updating an artist (all fields optional) */
export interface ArtistUpdate {
  name?: string
  bio?: string | null
  country?: string | null
}

/** Venue as returned by the API */
export interface VenueResponse {
  id: number
  name: string
  city: string
  country: string
  capacity: number | null
  created_at: string
}

/** Payload for creating a venue */
export interface VenueCreate {
  name: string
  city: string
  country: string
  capacity?: number | null
}

/** Payload for updating a venue (all fields optional) */
export interface VenueUpdate {
  name?: string
  city?: string
  country?: string
  capacity?: number | null
}

/** Concert as returned by the API */
export interface ConcertResponse {
  id: number
  title: string
  artist: ArtistResponse | null
  venue: VenueResponse | null
  /** ISO date string, e.g. "2024-06-15" */
  date: string
  setlist: string[] | null
  notes: string | null
  /** 1–5 */
  rating: number | null
  ticket_price: number | null
  currency: string
  created_at: string
  updated_at: string
}

/** Payload for creating a concert */
export interface ConcertCreate {
  title: string
  date: string
  artist_id?: number | null
  venue_id?: number | null
  setlist?: string[] | null
  notes?: string | null
  rating?: number | null
  ticket_price?: number | null
  currency?: string
}

/** Payload for updating a concert (all fields optional) */
export interface ConcertUpdate {
  title?: string
  date?: string
  artist_id?: number | null
  venue_id?: number | null
  setlist?: string[] | null
  notes?: string | null
  rating?: number | null
  ticket_price?: number | null
  currency?: string
}

/** Generic paginated list response */
export interface PaginatedResponse<T> {
  items: T[]
  total: number
  page: number
  page_size: number
  pages: number
}
