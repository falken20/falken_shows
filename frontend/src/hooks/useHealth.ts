import { useQuery } from '@tanstack/react-query'
import { healthApi } from '@/api/health'

export function useHealth() {
  return useQuery({
    queryKey: ['health'],
    queryFn: healthApi.getHealth,
    staleTime: 30 * 1000, // 30 seconds
    retry: false,
  })
}
