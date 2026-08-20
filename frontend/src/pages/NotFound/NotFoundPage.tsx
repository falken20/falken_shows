import Box from '@mui/material/Box'
import Button from '@mui/material/Button'
import Typography from '@mui/material/Typography'
import { Link as RouterLink } from 'react-router-dom'
import { useTranslation } from 'react-i18next'

/**
 * 404 page rendered by the catch-all `<Route path="*">` in {@link AppRouter}.
 *
 * Displays a large "404" heading, a localised error message, and a
 * "Back to Home" button that navigates to `/` using client-side routing.
 * The root element has `role="main"` for accessibility.
 */
export default function NotFoundPage() {
  const { t } = useTranslation()

  return (
    <Box
      sx={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        gap: 3,
        py: 12,
      }}
      role="main"
    >
      <Typography variant="h1" fontWeight={800} color="text.disabled">
        404
      </Typography>
      <Typography variant="h5" component="h2">
        {t('errors.notFound.title')}
      </Typography>
      <Typography variant="body1" color="text.secondary">
        {t('errors.notFound.message')}
      </Typography>
      <Button component={RouterLink} to="/" variant="contained" size="large">
        {t('errors.notFound.backHome')}
      </Button>
    </Box>
  )
}
