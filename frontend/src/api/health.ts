import { apiClient } from './client'

/** Response shape for `GET /api/v1/health`. */
export interface HealthResponse {
  status: 'ok' | 'degraded' | 'error'
  app_name: string
  version: string
  environment: string
}

/** Response shape for `GET /api/v1/ready`. */
export interface ReadinessResponse {
  status: 'ok' | 'degraded' | 'error'
  database: 'ok' | 'error'
}

/**
 * API functions for the system health endpoints.
 *
 * Used by {@link useHealth} to poll service status from the home page.
 */
export const healthApi = {
  getHealth: () => apiClient.get<HealthResponse>('/health').then(r => r.data),
  getReady: () => apiClient.get<ReadinessResponse>('/ready').then(r => r.data),
}
