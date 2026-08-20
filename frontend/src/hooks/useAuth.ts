import { useCallback, useState } from 'react'
import { authApi } from '@/api/concerts'

const TOKEN_KEY = 'live-memories-token'

/**
 * Simple auth hook that persists the JWT in `localStorage`.
 *
 * No Context Provider is required – each call reads directly from
 * `localStorage` so any component can call it independently.
 */
export function useAuth() {
  const [token, setToken] = useState<string | null>(() => localStorage.getItem(TOKEN_KEY))

  const login = useCallback(async (username: string, password: string): Promise<void> => {
    const response = await authApi.login(username, password)
    localStorage.setItem(TOKEN_KEY, response.access_token)
    setToken(response.access_token)
  }, [])

  const logout = useCallback((): void => {
    localStorage.removeItem(TOKEN_KEY)
    setToken(null)
  }, [])

  return {
    token,
    isAuthenticated: token !== null,
    login,
    logout,
  }
}
