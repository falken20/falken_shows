import { createContext, useCallback, useContext, useState, type ReactNode } from 'react'
import { createElement } from 'react'
import { authApi } from '@/api/concerts'
import { apiClient } from '@/api/client'

export const TOKEN_KEY = 'live-memories-token'

interface AuthContextValue {
  token: string | null
  isAuthenticated: boolean
  login: (username: string, password: string) => Promise<void>
  logout: () => Promise<void>
}

const AuthContext = createContext<AuthContextValue>({
  token: null,
  isAuthenticated: false,
  login: async () => {},
  logout: async () => {},
})

function readStoredToken(): string | null {
  return sessionStorage.getItem(TOKEN_KEY)
}

export function AuthProvider({ children }: { children: ReactNode }) {
  const [token, setToken] = useState<string | null>(() => readStoredToken())

  const login = useCallback(async (username: string, password: string): Promise<void> => {
    const response = await authApi.login(username, password)
    sessionStorage.setItem(TOKEN_KEY, response.access_token)
    setToken(response.access_token)
  }, [])

  const logout = useCallback(async (): Promise<void> => {
    try {
      await authApi.logout()
    } catch {
      // Client logout still proceeds if the token is already invalid.
    }
    sessionStorage.removeItem(TOKEN_KEY)
    setToken(null)
  }, [])

  return createElement(
    AuthContext.Provider,
    { value: { token, isAuthenticated: token !== null, login, logout } },
    children
  )
}

export function useAuth() {
  return useContext(AuthContext)
}

apiClient.interceptors.request.use(config => {
  const t = sessionStorage.getItem(TOKEN_KEY)
  if (t && config.headers) {
    config.headers.Authorization = `Bearer ${t}`
  }
  return config
})
