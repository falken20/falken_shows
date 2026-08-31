import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { concertsApi } from '@/api/concerts'
import type { ConcertCreate, ConcertUpdate } from '@/types'

const QUERY_KEY = 'concerts'

export function useConcerts(page = 1, pageSize = 20) {
  return useQuery({
    queryKey: [QUERY_KEY, page, pageSize],
    queryFn: () => concertsApi.getAll(page, pageSize),
  })
}

export function useConcert(id: number) {
  return useQuery({
    queryKey: [QUERY_KEY, id],
    queryFn: () => concertsApi.getById(id),
    enabled: id > 0,
  })
}

export function useCreateConcert() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (data: ConcertCreate) => concertsApi.create(data),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: [QUERY_KEY] })
    },
  })
}

export function useUpdateConcert() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: ({ id, data }: { id: number; data: ConcertUpdate }) => concertsApi.update(id, data),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: [QUERY_KEY] })
    },
  })
}

export function useDeleteConcert() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (id: number) => concertsApi.delete(id),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: [QUERY_KEY] })
    },
  })
}
