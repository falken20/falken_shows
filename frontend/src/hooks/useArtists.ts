import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { artistsApi } from '@/api/concerts'
import type { ArtistCreate, ArtistUpdate } from '@/types'

const QUERY_KEY = 'artists'

export function useArtists(page = 1, pageSize = 20) {
  return useQuery({
    queryKey: [QUERY_KEY, page, pageSize],
    queryFn: () => artistsApi.getAll(page, pageSize),
  })
}

export function useArtist(id: number) {
  return useQuery({
    queryKey: [QUERY_KEY, id],
    queryFn: () => artistsApi.getById(id),
    enabled: id > 0,
  })
}

export function useCreateArtist() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (data: ArtistCreate) => artistsApi.create(data),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: [QUERY_KEY] })
    },
  })
}

export function useUpdateArtist() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: ({ id, data }: { id: number; data: ArtistUpdate }) => artistsApi.update(id, data),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: [QUERY_KEY] })
    },
  })
}

export function useDeleteArtist() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (id: number) => artistsApi.delete(id),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: [QUERY_KEY] })
    },
  })
}
