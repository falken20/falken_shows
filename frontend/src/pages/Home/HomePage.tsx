import Alert from '@mui/material/Alert'
import Box from '@mui/material/Box'
import Chip from '@mui/material/Chip'
import CircularProgress from '@mui/material/CircularProgress'
import Paper from '@mui/material/Paper'
import Typography from '@mui/material/Typography'
import MusicNoteIcon from '@mui/icons-material/MusicNote'
import { useTranslation } from 'react-i18next'
import { useHealth } from '@/hooks/useHealth'

export default function HomePage() {
  const { t } = useTranslation()
  const { data, isLoading, isError } = useHealth()

  return (
    <Box
      sx={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        gap: 4,
        py: 8,
      }}
    >
      {/* Hero */}
      <Box sx={{ textAlign: 'center' }}>
        <MusicNoteIcon sx={{ fontSize: 72, color: 'primary.main', mb: 2 }} aria-hidden="true" />
        <Typography variant="h3" component="h1" fontWeight={800} gutterBottom>
          {t('app.name')}
        </Typography>
        <Typography variant="h6" color="text.secondary" sx={{ maxWidth: 480 }}>
          {t('home.tagline')}
        </Typography>
      </Box>

      {/* API health status */}
      <Paper
        elevation={2}
        sx={{ p: 3, width: '100%', maxWidth: 400 }}
        aria-label={t('home.apiStatus.label')}
      >
        <Typography variant="subtitle1" fontWeight={600} gutterBottom>
          {t('home.apiStatus.title')}
        </Typography>

        {isLoading && (
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <CircularProgress size={16} aria-hidden="true" />
            <Typography variant="body2">{t('common.loading')}</Typography>
          </Box>
        )}

        {isError && (
          <Alert severity="error" role="alert">
            {t('home.apiStatus.error')}
          </Alert>
        )}

        {data && (
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
              <Chip
                label={data.status.toUpperCase()}
                color={data.status === 'ok' ? 'success' : 'error'}
                size="small"
                aria-label={`${t('home.apiStatus.status')}: ${data.status}`}
              />
              <Typography variant="body2" color="text.secondary">
                {data.app_name} v{data.version}
              </Typography>
            </Box>
            <Typography variant="caption" color="text.secondary">
              {t('home.apiStatus.environment')}: {data.environment}
            </Typography>
          </Box>
        )}
      </Paper>
    </Box>
  )
}
