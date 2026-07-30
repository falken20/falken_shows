import AppBar from '@mui/material/AppBar'
import IconButton from '@mui/material/IconButton'
import Toolbar from '@mui/material/Toolbar'
import Typography from '@mui/material/Typography'
import Brightness4Icon from '@mui/icons-material/Brightness4'
import Brightness7Icon from '@mui/icons-material/Brightness7'
import MusicNoteIcon from '@mui/icons-material/MusicNote'
import { Link as RouterLink } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import { useThemeMode } from '@/hooks/useThemeMode'

export function TopBar() {
  const { t } = useTranslation()
  const { mode, toggleMode } = useThemeMode()

  return (
    <AppBar position="sticky" elevation={1}>
      <Toolbar>
        <MusicNoteIcon sx={{ mr: 1 }} aria-hidden="true" />
        <Typography
          variant="h6"
          component={RouterLink}
          to="/"
          sx={{
            flexGrow: 1,
            textDecoration: 'none',
            color: 'inherit',
            fontWeight: 700,
          }}
        >
          {t('app.name')}
        </Typography>
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
