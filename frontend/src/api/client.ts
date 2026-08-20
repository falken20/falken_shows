import axios, { type AxiosError } from 'axios'

/**
 * Resolve the API base URL in order of priority:
 * 1. `VITE_API_BASE_URL` build-time env var (set in Cloud Build for production).
 * 2. In Vite dev mode (`import.meta.env.DEV === true`): `http://localhost:8000/api/v1`.
 * 3. Production default: relative `/api/v1` (nginx proxies to Cloud Run backend).
 */
const DEFAULT_API_BASE_URL = import.meta.env.DEV ? 'http://localhost:8000/api/v1' : '/api/v1'
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? DEFAULT_API_BASE_URL

/**
 * Pre-configured Axios instance shared by all API modules.
 *
 * - Sets `Accept` and `Content-Type` headers so every request is treated as JSON.
 * - The response interceptor extracts the `error.message` field from the
 *   standard error envelope `{ error: { message } }` and rejects with a
 *   plain `Error`, making error handling uniform across all call sites.
 */
export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    Accept: 'application/json',
    'Content-Type': 'application/json',
  },
})

interface ApiErrorResponse {
  error?: { message?: string }
}

// Response interceptor for error handling
apiClient.interceptors.response.use(
  response => response,
  (error: AxiosError<ApiErrorResponse>) => {
    const message =
      error.response?.data?.error?.message ??
      error.message ??
      'An unexpected error occurred'
    return Promise.reject(new Error(message))
  },
)
