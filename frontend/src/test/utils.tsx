import type { ReactNode } from 'react'
import { render, type RenderOptions } from '@testing-library/react'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { BrowserRouter } from 'react-router-dom'
import { ThemeProvider } from '@mui/material/styles'
import CssBaseline from '@mui/material/CssBaseline'
import { createAppTheme } from '@/utils/theme'

/**
 * Create an isolated `QueryClient` for each test.
 *
 * Disables retries and `staleTime` so tests are deterministic and do not
 * depend on timing or cached data from previous test cases.
 */
function createTestQueryClient() {
  return new QueryClient({
    defaultOptions: {
      queries: {
        retry: false,
        staleTime: 0,
      },
    },
  })
}

/**
 * Wraps the component under test with the same providers used in production:
 * TanStack Query, MUI ThemeProvider (light mode), and BrowserRouter.
 */
// eslint-disable-next-line react-refresh/only-export-components -- test utility: provider and helpers co-located intentionally
function AppProviders({ children }: { children: ReactNode }) {
  const queryClient = createTestQueryClient()
  const theme = createAppTheme('light')

  return (
    <QueryClientProvider client={queryClient}>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <BrowserRouter>{children}</BrowserRouter>
      </ThemeProvider>
    </QueryClientProvider>
  )
}

/**
 * Drop-in replacement for RTL `render` that automatically wraps the component
 * in all application providers.
 *
 * @example
 * ```tsx
 * import { renderWithProviders, screen } from '@/test/utils'
 *
 * it('shows the title', () => {
 *   renderWithProviders(<MyComponent />)
 *   expect(screen.getByRole('heading')).toBeInTheDocument()
 * })
 * ```
 */
function renderWithProviders(ui: React.ReactElement, options?: Omit<RenderOptions, 'wrapper'>) {
  return render(ui, { wrapper: AppProviders, ...options })
}

// eslint-disable-next-line react-refresh/only-export-components -- test utility intentionally exports both components and helpers
export * from '@testing-library/react'
export { renderWithProviders }
