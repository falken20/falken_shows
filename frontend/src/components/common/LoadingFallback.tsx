import Box from '@mui/material/Box'
import CircularProgress from '@mui/material/CircularProgress'
import Typography from '@mui/material/Typography'
import { useTranslation } from 'react-i18next'

/**
 * Full-viewport loading indicator shown while lazy-loaded pages are fetching.
 *
 * Used as the `fallback` prop of `<Suspense>` in {@link App}. The outer `Box`
 * carries `role="status"` and a localised `aria-label` so screen readers
 * announce the loading state.
 */
export function LoadingFallback() {
  const { t } = useTranslation()

  return (
    <Box
      sx={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        minHeight: '100vh',
        gap: 2,
      }}
      role="status"
      aria-label={t('common.loading')}
    >
      <CircularProgress size={48} aria-hidden="true" />
      <Typography variant="body2" color="text.secondary">
        {t('common.loading')}
      </Typography>
    </Box>
  )
}
