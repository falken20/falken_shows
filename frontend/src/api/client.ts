import axios, { type AxiosError } from 'axios'

const DEFAULT_API_BASE_URL = import.meta.env.DEV ? 'http://localhost:8000/api/v1' : '/api/v1'
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? DEFAULT_API_BASE_URL

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
