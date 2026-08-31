import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { venuesApi } from '@/api/concerts'
import type { VenueCreate, VenueUpdate } from '@/types'

const QUERY_KEY = 'venues'

export function useVenues(page = 1, pageSize = 20) {
  return useQuery({
    queryKey: [QUERY_KEY, page, pageSize],
    queryFn: () => venuesApi.getAll(page, pageSize),
  })
}

export function useVenue(id: number) {
  return useQuery({
    queryKey: [QUERY_KEY, id],
    queryFn: () => venuesApi.getById(id),
    enabled: id > 0,
  })
}

export function useCreateVenue() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (data: VenueCreate) => venuesApi.create(data),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: [QUERY_KEY] })
    },
  })
}

export function useUpdateVenue() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: ({ id, data }: { id: number; data: VenueUpdate }) => venuesApi.update(id, data),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: [QUERY_KEY] })
    },
  })
}

export function useDeleteVenue() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (id: number) => venuesApi.delete(id),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: [QUERY_KEY] })
    },
  })
}
