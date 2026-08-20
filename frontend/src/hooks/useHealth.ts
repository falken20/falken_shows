import { useQuery } from '@tanstack/react-query'
import { healthApi } from '@/api/health'

/**
 * TanStack Query hook that fetches `GET /api/v1/health`.
 *
 * - Query key: `['health']` – cached across the app; invalidate with
 *   `queryClient.invalidateQueries({ queryKey: ['health'] })`.
 * - `staleTime: 30s` – prevents redundant refetches between page navigations.
 * - `retry: false` – a failed health check should surface immediately without
 *   hiding the error behind retry delays.
 *
 * @returns Standard TanStack Query result with `data`, `isLoading`, `isError`.
 */
export function useHealth() {
  return useQuery({
    queryKey: ['health'],
    queryFn: healthApi.getHealth,
    staleTime: 30 * 1000, // 30 seconds
    retry: false,
  })
}
