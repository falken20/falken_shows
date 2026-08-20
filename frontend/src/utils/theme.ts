import { createTheme } from '@mui/material/styles'
import type { PaletteMode } from '@mui/material'

/**
 * Create a MUI theme instance for the given palette mode.
 *
 * Design tokens:
 * - Primary: `#7c3aed` (purple-600) – evokes concert/music vibes.
 * - Secondary: `#f59e0b` (amber-500) – warm accent for CTAs.
 * - Font: Inter → Roboto → system fallback.
 * - Buttons: `textTransform: none` and `fontWeight: 600` for readability.
 *
 * Called on every mode change; MUI memoises the result internally.
 *
 * @param mode - `'light'` or `'dark'`.
 */
export function createAppTheme(mode: PaletteMode) {
  return createTheme({
    palette: {
      mode,
      primary: {
        main: '#7c3aed', // purple-600 – music/concert vibe
      },
      secondary: {
        main: '#f59e0b', // amber-500
      },
    },
    typography: {
      fontFamily: '"Inter", "Roboto", "Helvetica", "Arial", sans-serif',
    },
    shape: {
      borderRadius: 8,
    },
    components: {
      MuiButton: {
        styleOverrides: {
          root: {
            textTransform: 'none',
            fontWeight: 600,
          },
        },
      },
    },
  })
}
