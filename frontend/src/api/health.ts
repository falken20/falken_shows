import { apiClient } from './client'

export interface HealthResponse {
  status: 'ok' | 'degraded' | 'error'
  app_name: string
  version: string
  environment: string
}

export interface ReadinessResponse {
  status: 'ok' | 'degraded' | 'error'
  database: 'ok' | 'error'
}

export const healthApi = {
  getHealth: () => apiClient.get<HealthResponse>('/health').then(r => r.data),
  getReady: () => apiClient.get<ReadinessResponse>('/ready').then(r => r.data),
}
