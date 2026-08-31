import { apiClient } from './client'
import type { HealthResponse, ReadinessResponse } from '@/types'

export type { HealthResponse, ReadinessResponse }

export const healthApi = {
  getHealth: () => apiClient.get<HealthResponse>('/health').then(r => r.data),
  getReady: () => apiClient.get<ReadinessResponse>('/ready').then(r => r.data),
}
