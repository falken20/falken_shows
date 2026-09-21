import AppBar from '@mui/material/AppBar'
import Box from '@mui/material/Box'
import Button from '@mui/material/Button'
import IconButton from '@mui/material/IconButton'
import Toolbar from '@mui/material/Toolbar'
import Typography from '@mui/material/Typography'
import Brightness4Icon from '@mui/icons-material/Brightness4'
import Brightness7Icon from '@mui/icons-material/Brightness7'
import MusicNoteIcon from '@mui/icons-material/MusicNote'
import { Link as RouterLink, useNavigate } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import { useThemeMode } from '@/hooks/useThemeMode'
import { useAuth } from '@/hooks/useAuth'

/**
 * Sticky application header displayed on every page inside {@link MainLayout}.
 *
 * Contains:
 * - App logo and title (links to `/`).
 * - Light/dark mode toggle button (persisted to `localStorage` via
 *   {@link useThemeMode}). The button label is localised and toggled
 *   between `theme.switchToLight` and `theme.switchToDark`.
 *
 * Accessibility: decorative icons have `aria-hidden="true"` so screen
 * readers focus on the meaningful button label.
 */
export function TopBar() {
  const { t } = useTranslation()
  const { mode, toggleMode } = useThemeMode()
  const { isAuthenticated, logout } = useAuth()
  const navigate = useNavigate()

  return (
    <AppBar position="sticky" elevation={1}>
      <Toolbar sx={{ flexWrap: 'wrap', gap: { xs: 0.5, sm: 1 }, py: { xs: 1, sm: 0.5 } }}>
        <MusicNoteIcon sx={{ mr: 1 }} aria-hidden="true" />
        <Typography
          variant="h6"
          component={RouterLink}
          to="/"
          sx={{
            flexGrow: 1,
            minWidth: 0,
            textDecoration: 'none',
            color: 'inherit',
            fontWeight: 700,
          }}
        >
          {t('app.name')}
        </Typography>
        <Box sx={{ display: 'flex', flexWrap: 'wrap', justifyContent: 'flex-end', gap: 0.5 }}>
          <Button
            component={RouterLink}
            to="/concerts"
            color="inherit"
            aria-label={t('concerts.nav')}
          >
            {t('concerts.nav')}
          </Button>
          {isAuthenticated ? (
            <Button
              color="inherit"
              onClick={() => {
                void logout().then(() => navigate('/login'))
              }}
              aria-label={t('auth.logout')}
            >
              {t('auth.logout')}
            </Button>
          ) : (
            <Button component={RouterLink} to="/login" color="inherit" aria-label={t('auth.login')}>
              {t('auth.login')}
            </Button>
          )}
        </Box>
        <IconButton
          color="inherit"
          onClick={toggleMode}
          aria-label={mode === 'dark' ? t('theme.switchToLight') : t('theme.switchToDark')}
        >
          {mode === 'dark' ? (
            <Brightness7Icon aria-hidden="true" />
          ) : (
            <Brightness4Icon aria-hidden="true" />
          )}
        </IconButton>
      </Toolbar>
    </AppBar>
  )
}
