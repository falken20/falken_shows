import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { ReactQueryDevtools } from '@tanstack/react-query-devtools'
import { BrowserRouter } from 'react-router-dom'
import CssBaseline from '@mui/material/CssBaseline'
import { ThemeProvider } from '@mui/material/styles'
import { Suspense } from 'react'
import { useThemeMode } from '@/hooks/useThemeMode'
import { createAppTheme } from '@/utils/theme'
import AppRouter from '@/router/AppRouter'
import { LoadingFallback } from '@/components/common/LoadingFallback'

/**
 * Global TanStack Query client.
 *
 * - `staleTime: 5 min` – avoids refetching data that is unlikely to change
 *   between navigations.
 * - `retry: 1` – retries failed requests once before surfacing the error,
 *   reducing noise from transient network issues.
 */
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 60 * 1000, // 5 minutes
      retry: 1,
    },
  },
})

/**
 * Inner component that reads the current theme mode and wraps the router.
 *
 * Separated from `App` so that `ThemeProvider` can consume `useThemeMode`
 * which requires `ThemeModeProvider` to be in the tree. `ThemeModeProvider`
 * is rendered by `main.tsx`, wrapping the entire `<App>`.
 */
function ThemedApp() {
  const { mode } = useThemeMode()
  const theme = createAppTheme(mode)

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <BrowserRouter>
        <Suspense fallback={<LoadingFallback />}>
          <AppRouter />
        </Suspense>
      </BrowserRouter>
    </ThemeProvider>
  )
}

/**
 * Application root component.
 *
 * Provides the global `QueryClientProvider` and renders `ThemedApp`.
 * `ReactQueryDevtools` is included unconditionally but only renders in
 * development builds.
 */
export default function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <ThemedApp />
      <ReactQueryDevtools initialIsOpen={false} />
    </QueryClientProvider>
  )
}
