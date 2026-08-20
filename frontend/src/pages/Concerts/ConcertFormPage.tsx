import Alert from '@mui/material/Alert'
import Box from '@mui/material/Box'
import Button from '@mui/material/Button'
import CircularProgress from '@mui/material/CircularProgress'
import MenuItem from '@mui/material/MenuItem'
import Paper from '@mui/material/Paper'
import Stack from '@mui/material/Stack'
import TextField from '@mui/material/TextField'
import Typography from '@mui/material/Typography'
import ArrowBackIcon from '@mui/icons-material/ArrowBack'
import { useEffect } from 'react'
import { Controller, useForm } from 'react-hook-form'
import { useNavigate, useParams } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import { useConcert, useCreateConcert, useUpdateConcert } from '@/hooks/useConcerts'
import { useArtists } from '@/hooks/useArtists'
import { useVenues } from '@/hooks/useVenues'
import { useAuth } from '@/hooks/useAuth'

interface ConcertFormValues {
  title: string
  date: string
  artist_id: number | null
  venue_id: number | null
  rating: number | null
  notes: string
  ticket_price: number | null
  currency: string
}

function normalizeDateForInput(value: string): string {
  if (value.includes('T')) {
    return value.split('T')[0]
  }
  return value
}

function normalizeDateForApi(value: string): string {
  if (value.includes('T')) {
    return value
  }
  return `${value}T00:00:00`
}

/**
 * Create/edit form for a concert.
 *
 * Mounted at `/concerts/new` (create) and `/concerts/:id/edit` (update).
 * Redirects unauthenticated users to the home page.
 */
export default function ConcertFormPage() {
  const { t } = useTranslation()
  const { id } = useParams<{ id?: string }>()
  const navigate = useNavigate()
  const { isAuthenticated } = useAuth()

  const isEditing = id !== undefined
  const numericId = isEditing ? Number(id) : 0

  // Redirect if not authenticated
  useEffect(() => {
    if (!isAuthenticated) {
      void navigate('/', { replace: true })
    }
  }, [isAuthenticated, navigate])

  const { data: existing, isLoading: loadingConcert } = useConcert(numericId)
  const { data: artistsData } = useArtists(1, 100)
  const { data: venuesData } = useVenues(1, 100)

  const createMutation = useCreateConcert()
  const updateMutation = useUpdateConcert()

  const {
    control,
    handleSubmit,
    reset,
    formState: { errors, isSubmitting },
  } = useForm<ConcertFormValues>({
    defaultValues: {
      title: '',
      date: '',
      artist_id: null,
      venue_id: null,
      rating: null,
      notes: '',
      ticket_price: null,
      currency: 'EUR',
    },
  })

  // Populate form when editing an existing concert
  useEffect(() => {
    if (existing) {
      reset({
        title: existing.title,
        date: normalizeDateForInput(existing.date),
        artist_id: existing.artist?.id ?? null,
        venue_id: existing.venue?.id ?? null,
        rating: existing.rating ?? null,
        notes: existing.notes ?? '',
        ticket_price: existing.ticket_price ?? null,
        currency: existing.currency,
      })
    }
  }, [existing, reset])

  const onSubmit = async (values: ConcertFormValues) => {
    const payload = {
      ...values,
      date: normalizeDateForApi(values.date),
      notes: values.notes || null,
    }
    if (isEditing) {
      const result = await updateMutation.mutateAsync({ id: numericId, data: payload })
      void navigate(`/concerts/${result.id}`)
    } else {
      const result = await createMutation.mutateAsync(payload)
      void navigate(`/concerts/${result.id}`)
    }
  }

  const mutationError = createMutation.error ?? updateMutation.error

  if (isEditing && loadingConcert) {
    return (
      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, py: 4, px: { xs: 2, sm: 4 } }}>
        <CircularProgress size={20} aria-hidden="true" />
        <Typography variant="body2">{t('common.loading')}</Typography>
      </Box>
    )
  }

  return (
    <Box sx={{ py: 4, px: { xs: 2, sm: 4 }, maxWidth: 600, mx: 'auto' }}>
      {/* Back */}
      <Button
        startIcon={<ArrowBackIcon aria-hidden="true" />}
        onClick={() => {
          void navigate(isEditing ? `/concerts/${numericId}` : '/concerts')
        }}
        sx={{ mb: 2 }}
        aria-label={t('common.back')}
      >
        {t('common.back')}
      </Button>

      <Paper elevation={2} sx={{ p: 3 }}>
        <Typography variant="h5" component="h1" fontWeight={700} mb={3}>
          {isEditing ? t('concerts.form.editTitle') : t('concerts.form.createTitle')}
        </Typography>

        {mutationError && (
          <Alert severity="error" role="alert" sx={{ mb: 2 }}>
            {t('errors.generic')}
          </Alert>
        )}

        <Box
          component="form"
          noValidate
          onSubmit={e => {
            void handleSubmit(onSubmit)(e)
          }}
          aria-label={isEditing ? t('concerts.form.editTitle') : t('concerts.form.createTitle')}
        >
          <Stack spacing={2}>
            {/* Title */}
            <Controller
              name="title"
              control={control}
              rules={{ required: true }}
              render={({ field }) => (
                <TextField
                  {...field}
                  label={t('concerts.form.title')}
                  required
                  fullWidth
                  error={Boolean(errors.title)}
                  helperText={errors.title ? t('common.required') : undefined}
                  inputProps={{ 'aria-required': true }}
                />
              )}
            />

            {/* Date */}
            <Controller
              name="date"
              control={control}
              rules={{ required: true }}
              render={({ field }) => (
                <TextField
                  {...field}
                  label={t('concerts.form.date')}
                  required
                  fullWidth
                  type="date"
                  error={Boolean(errors.date)}
                  helperText={errors.date ? t('common.required') : undefined}
                  InputLabelProps={{ shrink: true }}
                  inputProps={{ 'aria-required': true }}
                />
              )}
            />

            {/* Artist */}
            <Controller
              name="artist_id"
              control={control}
              render={({ field }) => (
                <TextField
                  {...field}
                  select
                  label={t('concerts.form.artist')}
                  fullWidth
                  value={field.value ?? ''}
                  onChange={e =>
                    field.onChange(e.target.value === '' ? null : Number(e.target.value))
                  }
                >
                  <MenuItem value="">—</MenuItem>
                  {artistsData?.items.map(a => (
                    <MenuItem key={a.id} value={a.id}>
                      {a.name}
                    </MenuItem>
                  ))}
                </TextField>
              )}
            />

            {/* Venue */}
            <Controller
              name="venue_id"
              control={control}
              render={({ field }) => (
                <TextField
                  {...field}
                  select
                  label={t('concerts.form.venue')}
                  fullWidth
                  value={field.value ?? ''}
                  onChange={e =>
                    field.onChange(e.target.value === '' ? null : Number(e.target.value))
                  }
                >
                  <MenuItem value="">—</MenuItem>
                  {venuesData?.items.map(v => (
                    <MenuItem key={v.id} value={v.id}>
                      {v.name}, {v.city}
                    </MenuItem>
                  ))}
                </TextField>
              )}
            />

            {/* Rating */}
            <Controller
              name="rating"
              control={control}
              render={({ field }) => (
                <TextField
                  {...field}
                  select
                  label={t('concerts.form.rating')}
                  fullWidth
                  value={field.value ?? ''}
                  onChange={e =>
                    field.onChange(e.target.value === '' ? null : Number(e.target.value))
                  }
                >
                  <MenuItem value="">—</MenuItem>
                  {[1, 2, 3, 4, 5].map(n => (
                    <MenuItem key={n} value={n}>
                      {n}
                    </MenuItem>
                  ))}
                </TextField>
              )}
            />

            {/* Ticket price & currency */}
            <Stack direction="row" spacing={2}>
              <Controller
                name="ticket_price"
                control={control}
                render={({ field }) => (
                  <TextField
                    {...field}
                    label={t('concerts.form.ticketPrice')}
                    fullWidth
                    type="number"
                    value={field.value ?? ''}
                    onChange={e =>
                      field.onChange(e.target.value === '' ? null : Number(e.target.value))
                    }
                    inputProps={{ min: 0, step: 0.01 }}
                  />
                )}
              />
              <Controller
                name="currency"
                control={control}
                render={({ field }) => (
                  <TextField
                    {...field}
                    label={t('concerts.form.currency')}
                    sx={{ width: 120 }}
                    inputProps={{ maxLength: 3, 'aria-label': t('concerts.form.currency') }}
                  />
                )}
              />
            </Stack>

            {/* Notes */}
            <Controller
              name="notes"
              control={control}
              render={({ field }) => (
                <TextField
                  {...field}
                  label={t('concerts.form.notes')}
                  fullWidth
                  multiline
                  rows={4}
                  value={field.value ?? ''}
                />
              )}
            />

            {/* Submit */}
            <Stack direction="row" spacing={2} justifyContent="flex-end">
              <Button
                onClick={() => {
                  void navigate(isEditing ? `/concerts/${numericId}` : '/concerts')
                }}
                aria-label={t('common.cancel')}
              >
                {t('common.cancel')}
              </Button>
              <Button
                type="submit"
                variant="contained"
                disabled={isSubmitting}
                aria-label={t('common.save')}
              >
                {isSubmitting ? (
                  <CircularProgress size={20} aria-hidden="true" />
                ) : (
                  t('common.save')
                )}
              </Button>
            </Stack>
          </Stack>
        </Box>
      </Paper>
    </Box>
  )
}
