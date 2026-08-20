import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { venuesApi } from '@/api/concerts'
import { useAuth } from '@/hooks/useAuth'
import type { VenueCreate, VenueUpdate } from '@/types'

const QUERY_KEY = 'venues'

/** Fetch a paginated list of venues. */
export function useVenues(page = 1, pageSize = 20) {
  return useQuery({
    queryKey: [QUERY_KEY, page, pageSize],
    queryFn: () => venuesApi.getAll(page, pageSize),
  })
}

/** Fetch a single venue by id. */
export function useVenue(id: number) {
  return useQuery({
    queryKey: [QUERY_KEY, id],
    queryFn: () => venuesApi.getById(id),
    enabled: id > 0,
  })
}

/** Mutation to create a venue. Invalidates the venues list on success. */
export function useCreateVenue() {
  const queryClient = useQueryClient()
  const { token } = useAuth()

  return useMutation({
    mutationFn: (data: VenueCreate) => venuesApi.create(data, token ?? ''),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: [QUERY_KEY] })
    },
  })
}

/** Mutation to update a venue. Invalidates the venues list on success. */
export function useUpdateVenue() {
  const queryClient = useQueryClient()
  const { token } = useAuth()

  return useMutation({
    mutationFn: ({ id, data }: { id: number; data: VenueUpdate }) =>
      venuesApi.update(id, data, token ?? ''),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: [QUERY_KEY] })
    },
  })
}

/** Mutation to delete a venue. Invalidates the venues list on success. */
export function useDeleteVenue() {
  const queryClient = useQueryClient()
  const { token } = useAuth()

  return useMutation({
    mutationFn: (id: number) => venuesApi.delete(id, token ?? ''),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: [QUERY_KEY] })
    },
  })
}
