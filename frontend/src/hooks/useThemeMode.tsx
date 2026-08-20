import { createContext, useContext, useEffect, useState } from 'react'
import type { PaletteMode } from '@mui/material'

const STORAGE_KEY = 'live-memories-theme-mode'

interface ThemeModeContextValue {
  mode: PaletteMode
  /** Toggle between `'light'` and `'dark'` mode and persist to localStorage. */
  toggleMode: () => void
}

const ThemeModeContext = createContext<ThemeModeContextValue>({
  mode: 'light',
  toggleMode: () => undefined,
})

/**
 * Context provider for light/dark theme mode.
 *
 * Initialisation priority:
 * 1. Value stored in `localStorage` under {@link STORAGE_KEY}.
 * 2. OS-level `prefers-color-scheme` media query.
 * 3. Default: `'light'`.
 *
 * Place this provider high in the tree (e.g. wrapping `<App>` in `main.tsx`)
 * so that `useThemeMode` is available everywhere.
 */
export function ThemeModeProvider({ children }: { children: React.ReactNode }) {
  const [mode, setMode] = useState<PaletteMode>(() => {
    const stored = localStorage.getItem(STORAGE_KEY)
    if (stored === 'light' || stored === 'dark') return stored
    return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'
  })

  useEffect(() => {
    localStorage.setItem(STORAGE_KEY, mode)
  }, [mode])

  const toggleMode = () => setMode(prev => (prev === 'light' ? 'dark' : 'light'))

  return (
    <ThemeModeContext.Provider value={{ mode, toggleMode }}>
      {children}
    </ThemeModeContext.Provider>
  )
}

// eslint-disable-next-line react-refresh/only-export-components -- provider and hook intentionally co-located
/**
 * Consume the current theme mode and toggle function.
 *
 * Must be used inside a {@link ThemeModeProvider}.
 */
export function useThemeMode() {
  return useContext(ThemeModeContext)
}
