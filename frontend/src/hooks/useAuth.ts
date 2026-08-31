import { createContext, useCallback, useContext, useState, type ReactNode } from 'react'
import { createElement } from 'react'
import { authApi } from '@/api/concerts'
import { apiClient } from '@/api/client'

const TOKEN_KEY = 'live-memories-token'

interface AuthContextValue {
  token: string | null
  isAuthenticated: boolean
  login: (username: string, password: string) => Promise<void>
  logout: () => void
}

const AuthContext = createContext<AuthContextValue>({
  token: null,
  isAuthenticated: false,
  login: async () => {},
  logout: () => {},
})

export function AuthProvider({ children }: { children: ReactNode }) {
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

  return createElement(
    AuthContext.Provider,
    { value: { token, isAuthenticated: token !== null, login, logout } },
    children
  )
}

export function useAuth() {
  return useContext(AuthContext)
}

// Axios request interceptor: attach token automatically
apiClient.interceptors.request.use(config => {
  const t = localStorage.getItem(TOKEN_KEY)
  if (t && config.headers) {
    config.headers.Authorization = `Bearer ${t}`
  }
  return config
})
