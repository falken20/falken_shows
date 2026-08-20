import Alert from '@mui/material/Alert'
import Box from '@mui/material/Box'
import Button from '@mui/material/Button'
import Chip from '@mui/material/Chip'
import CircularProgress from '@mui/material/CircularProgress'
import Dialog from '@mui/material/Dialog'
import DialogActions from '@mui/material/DialogActions'
import DialogContent from '@mui/material/DialogContent'
import DialogTitle from '@mui/material/DialogTitle'
import Divider from '@mui/material/Divider'
import Paper from '@mui/material/Paper'
import Rating from '@mui/material/Rating'
import Stack from '@mui/material/Stack'
import Typography from '@mui/material/Typography'
import ArrowBackIcon from '@mui/icons-material/ArrowBack'
import DeleteIcon from '@mui/icons-material/Delete'
import EditIcon from '@mui/icons-material/Edit'
import { useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import { useConcert, useDeleteConcert } from '@/hooks/useConcerts'
import { useAuth } from '@/hooks/useAuth'

/**
 * Detail page for a single concert at `/concerts/:id`.
 *
 * Shows all concert fields. Authenticated users can navigate to the edit page
 * or delete the concert (with a confirmation dialog).
 */
export default function ConcertDetailPage() {
  const { t } = useTranslation()
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const { isAuthenticated } = useAuth()
  const [deleteOpen, setDeleteOpen] = useState(false)

  const numericId = Number(id)
  const { data: concert, isLoading, isError } = useConcert(numericId)
  const deleteMutation = useDeleteConcert()

  const handleDelete = () => {
    void deleteMutation.mutateAsync(numericId).then(() => {
      setDeleteOpen(false)
      void navigate('/concerts')
    })
  }

  if (isLoading) {
    return (
      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, py: 4, px: { xs: 2, sm: 4 } }}>
        <CircularProgress size={20} aria-hidden="true" />
        <Typography variant="body2">{t('common.loading')}</Typography>
      </Box>
    )
  }

  if (isError || !concert) {
    return (
      <Box sx={{ py: 4, px: { xs: 2, sm: 4 } }}>
        <Alert severity="error" role="alert">
          {t('errors.generic')}
        </Alert>
      </Box>
    )
  }

  return (
    <Box sx={{ py: 4, px: { xs: 2, sm: 4 }, maxWidth: 720, mx: 'auto' }}>
      {/* Back navigation */}
      <Button
        startIcon={<ArrowBackIcon aria-hidden="true" />}
        onClick={() => { void navigate('/concerts') }}
        sx={{ mb: 2 }}
        aria-label={t('common.back')}
      >
        {t('common.back')}
      </Button>

      <Paper elevation={2} sx={{ p: 3 }}>
        {/* Title & actions */}
        <Stack direction="row" alignItems="flex-start" justifyContent="space-between" mb={2}>
          <Typography variant="h4" component="h1" fontWeight={700}>
            {concert.title}
          </Typography>
          {isAuthenticated && (
            <Stack direction="row" spacing={1}>
              <Button
                variant="outlined"
                startIcon={<EditIcon aria-hidden="true" />}
                onClick={() => { void navigate(`/concerts/${concert.id}/edit`) }}
                aria-label={t('common.edit')}
              >
                {t('common.edit')}
              </Button>
              <Button
                variant="outlined"
                color="error"
                startIcon={<DeleteIcon aria-hidden="true" />}
                onClick={() => setDeleteOpen(true)}
                aria-label={t('common.delete')}
              >
                {t('common.delete')}
              </Button>
            </Stack>
          )}
        </Stack>

        <Divider sx={{ mb: 2 }} />

        {/* Details */}
        <Stack spacing={1.5}>
          <Stack direction="row" spacing={1} alignItems="center">
            <Typography variant="body2" color="text.secondary" sx={{ minWidth: 120 }}>
              {t('concerts.form.date')}
            </Typography>
            <Typography variant="body1">{concert.date}</Typography>
          </Stack>

          {concert.artist && (
            <Stack direction="row" spacing={1} alignItems="center">
              <Typography variant="body2" color="text.secondary" sx={{ minWidth: 120 }}>
                {t('concerts.form.artist')}
              </Typography>
              <Typography variant="body1">{concert.artist.name}</Typography>
              {concert.artist.country && (
                <Chip label={concert.artist.country} size="small" />
              )}
            </Stack>
          )}

          {concert.venue && (
            <Stack direction="row" spacing={1} alignItems="center">
              <Typography variant="body2" color="text.secondary" sx={{ minWidth: 120 }}>
                {t('concerts.form.venue')}
              </Typography>
              <Typography variant="body1">
                {concert.venue.name}, {concert.venue.city}
              </Typography>
            </Stack>
          )}

          {concert.rating !== null && (
            <Stack direction="row" spacing={1} alignItems="center">
              <Typography variant="body2" color="text.secondary" sx={{ minWidth: 120 }}>
                {t('concerts.form.rating')}
              </Typography>
              <Rating
                value={concert.rating}
                readOnly
                aria-label={`${t('concerts.form.rating')}: ${concert.rating}/5`}
              />
            </Stack>
          )}

          {concert.ticket_price !== null && (
            <Stack direction="row" spacing={1} alignItems="center">
              <Typography variant="body2" color="text.secondary" sx={{ minWidth: 120 }}>
                {t('concerts.form.ticketPrice')}
              </Typography>
              <Typography variant="body1">
                {concert.ticket_price} {concert.currency}
              </Typography>
            </Stack>
          )}

          {concert.notes && (
            <>
              <Divider />
              <Stack spacing={0.5}>
                <Typography variant="body2" color="text.secondary">
                  {t('concerts.form.notes')}
                </Typography>
                <Typography variant="body1" sx={{ whiteSpace: 'pre-wrap' }}>
                  {concert.notes}
                </Typography>
              </Stack>
            </>
          )}

          {concert.setlist && concert.setlist.length > 0 && (
            <>
              <Divider />
              <Stack spacing={0.5}>
                <Typography variant="body2" color="text.secondary">
                  Setlist
                </Typography>
                <Stack direction="row" flexWrap="wrap" gap={1}>
                  {concert.setlist.map((song, idx) => (
                    <Chip key={idx} label={`${idx + 1}. ${song}`} size="small" />
                  ))}
                </Stack>
              </Stack>
            </>
          )}
        </Stack>
      </Paper>

      {/* Delete confirmation dialog */}
      <Dialog
        open={deleteOpen}
        onClose={() => setDeleteOpen(false)}
        aria-labelledby="delete-dialog-title"
      >
        <DialogTitle id="delete-dialog-title">{t('common.confirm')}</DialogTitle>
        <DialogContent>
          <Typography>{t('concerts.detail.deleteConfirm')}</Typography>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDeleteOpen(false)} aria-label={t('common.cancel')}>
            {t('common.cancel')}
          </Button>
          <Button
            color="error"
            variant="contained"
            onClick={() => { handleDelete() }}
            disabled={deleteMutation.isPending}
            aria-label={t('common.delete')}
          >
            {deleteMutation.isPending ? (
              <CircularProgress size={20} aria-hidden="true" />
            ) : (
              t('common.delete')
            )}
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  )
}
