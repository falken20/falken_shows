import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { concertsApi } from '@/api/concerts'
import { useAuth } from '@/hooks/useAuth'
import type { ConcertCreate, ConcertUpdate } from '@/types'

const QUERY_KEY = 'concerts'

/** Fetch a paginated list of concerts. */
export function useConcerts(page = 1, pageSize = 20) {
  return useQuery({
    queryKey: [QUERY_KEY, page, pageSize],
    queryFn: () => concertsApi.getAll(page, pageSize),
  })
}

/** Fetch a single concert by id. */
export function useConcert(id: number) {
  return useQuery({
    queryKey: [QUERY_KEY, id],
    queryFn: () => concertsApi.getById(id),
    enabled: id > 0,
  })
}

/** Mutation to create a concert. Invalidates the concerts list on success. */
export function useCreateConcert() {
  const queryClient = useQueryClient()
  const { token } = useAuth()

  return useMutation({
    mutationFn: (data: ConcertCreate) => concertsApi.create(data, token ?? ''),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: [QUERY_KEY] })
    },
  })
}

/** Mutation to update a concert. Invalidates the concerts list on success. */
export function useUpdateConcert() {
  const queryClient = useQueryClient()
  const { token } = useAuth()

  return useMutation({
    mutationFn: ({ id, data }: { id: number; data: ConcertUpdate }) =>
      concertsApi.update(id, data, token ?? ''),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: [QUERY_KEY] })
    },
  })
}

/** Mutation to delete a concert. Invalidates the concerts list on success. */
export function useDeleteConcert() {
  const queryClient = useQueryClient()
  const { token } = useAuth()

  return useMutation({
    mutationFn: (id: number) => concertsApi.delete(id, token ?? ''),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: [QUERY_KEY] })
    },
  })
}
