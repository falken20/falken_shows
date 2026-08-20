import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { artistsApi } from '@/api/concerts'
import { useAuth } from '@/hooks/useAuth'
import type { ArtistCreate, ArtistUpdate } from '@/types'

const QUERY_KEY = 'artists'

/** Fetch a paginated list of artists. */
export function useArtists(page = 1, pageSize = 20) {
  return useQuery({
    queryKey: [QUERY_KEY, page, pageSize],
    queryFn: () => artistsApi.getAll(page, pageSize),
  })
}

/** Fetch a single artist by id. */
export function useArtist(id: number) {
  return useQuery({
    queryKey: [QUERY_KEY, id],
    queryFn: () => artistsApi.getById(id),
    enabled: id > 0,
  })
}

/** Mutation to create an artist. Invalidates the artists list on success. */
export function useCreateArtist() {
  const queryClient = useQueryClient()
  const { token } = useAuth()

  return useMutation({
    mutationFn: (data: ArtistCreate) => artistsApi.create(data, token ?? ''),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: [QUERY_KEY] })
    },
  })
}

/** Mutation to update an artist. Invalidates the artists list on success. */
export function useUpdateArtist() {
  const queryClient = useQueryClient()
  const { token } = useAuth()

  return useMutation({
    mutationFn: ({ id, data }: { id: number; data: ArtistUpdate }) =>
      artistsApi.update(id, data, token ?? ''),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: [QUERY_KEY] })
    },
  })
}

/** Mutation to delete an artist. Invalidates the artists list on success. */
export function useDeleteArtist() {
  const queryClient = useQueryClient()
  const { token } = useAuth()

  return useMutation({
    mutationFn: (id: number) => artistsApi.delete(id, token ?? ''),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: [QUERY_KEY] })
    },
  })
}
