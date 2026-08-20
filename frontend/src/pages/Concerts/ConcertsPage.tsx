import Alert from '@mui/material/Alert'
import Box from '@mui/material/Box'
import Button from '@mui/material/Button'
import CircularProgress from '@mui/material/CircularProgress'
import Paper from '@mui/material/Paper'
import Rating from '@mui/material/Rating'
import Stack from '@mui/material/Stack'
import Table from '@mui/material/Table'
import TableBody from '@mui/material/TableBody'
import TableCell from '@mui/material/TableCell'
import TableHead from '@mui/material/TableHead'
import TableRow from '@mui/material/TableRow'
import Typography from '@mui/material/Typography'
import AddIcon from '@mui/icons-material/Add'
import { useState } from 'react'
import { Link as RouterLink, useNavigate } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import { useConcerts } from '@/hooks/useConcerts'
import { useAuth } from '@/hooks/useAuth'

/**
 * List page for concerts at `/concerts`.
 *
 * Displays a paginated MUI table of all concerts.  Authenticated users see
 * an "Add concert" button.  Clicking a row navigates to the detail page.
 */
export default function ConcertsPage() {
  const { t } = useTranslation()
  const navigate = useNavigate()
  const { isAuthenticated } = useAuth()
  const [page, setPage] = useState(1)
  const PAGE_SIZE = 20

  const { data, isLoading, isError } = useConcerts(page, PAGE_SIZE)

  return (
    <Box sx={{ py: 4, px: { xs: 2, sm: 4 } }}>
      {/* Header */}
      <Stack direction="row" alignItems="center" justifyContent="space-between" mb={3}>
        <Typography variant="h4" component="h1" fontWeight={700}>
          {t('concerts.title')}
        </Typography>
        {isAuthenticated && (
          <Button
            variant="contained"
            startIcon={<AddIcon aria-hidden="true" />}
            component={RouterLink}
            to="/concerts/new"
            aria-label={t('concerts.addNew')}
          >
            {t('concerts.addNew')}
          </Button>
        )}
      </Stack>

      {/* Loading */}
      {isLoading && (
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          <CircularProgress size={20} aria-hidden="true" />
          <Typography variant="body2">{t('common.loading')}</Typography>
        </Box>
      )}

      {/* Error */}
      {isError && (
        <Alert severity="error" role="alert">
          {t('errors.network')}
        </Alert>
      )}

      {/* Empty state */}
      {data && data.items.length === 0 && (
        <Typography color="text.secondary" sx={{ mt: 4, textAlign: 'center' }}>
          {t('concerts.empty')}
        </Typography>
      )}

      {/* Table */}
      {data && data.items.length > 0 && (
        <Paper elevation={2}>
          <Table aria-label={t('concerts.title')}>
            <TableHead>
              <TableRow>
                <TableCell>{t('concerts.form.title')}</TableCell>
                <TableCell>{t('concerts.form.artist')}</TableCell>
                <TableCell>{t('concerts.form.venue')}</TableCell>
                <TableCell>{t('concerts.form.date')}</TableCell>
                <TableCell>{t('concerts.form.rating')}</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {data.items.map(concert => (
                <TableRow
                  key={concert.id}
                  hover
                  sx={{ cursor: 'pointer' }}
                  onClick={() => {
                    void navigate(`/concerts/${concert.id}`)
                  }}
                  tabIndex={0}
                  onKeyDown={e => {
                    if (e.key === 'Enter' || e.key === ' ') void navigate(`/concerts/${concert.id}`)
                  }}
                  aria-label={concert.title}
                >
                  <TableCell>{concert.title}</TableCell>
                  <TableCell>{concert.artist?.name ?? '—'}</TableCell>
                  <TableCell>
                    {concert.venue ? `${concert.venue.name}, ${concert.venue.city}` : '—'}
                  </TableCell>
                  <TableCell>{concert.date}</TableCell>
                  <TableCell>
                    {concert.rating !== null ? (
                      <Rating
                        value={concert.rating}
                        readOnly
                        size="small"
                        aria-label={`${concert.rating}/5`}
                      />
                    ) : (
                      '—'
                    )}
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>

          {/* Pagination */}
          <Stack
            direction="row"
            alignItems="center"
            justifyContent="center"
            spacing={2}
            sx={{ py: 2 }}
          >
            <Button
              disabled={page <= 1}
              onClick={() => setPage(p => p - 1)}
              aria-label={t('common.previous')}
            >
              {t('common.previous')}
            </Button>
            <Typography variant="body2">
              {`${t('common.page', { defaultValue: 'Página' })} ${data.page} / ${data.pages}`}
            </Typography>
            <Button
              disabled={page >= data.pages}
              onClick={() => setPage(p => p + 1)}
              aria-label={t('common.next')}
            >
              {t('common.next')}
            </Button>
          </Stack>
        </Paper>
      )}
    </Box>
  )
}
