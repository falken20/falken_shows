import Alert from '@mui/material/Alert'
import Box from '@mui/material/Box'
import Button from '@mui/material/Button'
import Paper from '@mui/material/Paper'
import Stack from '@mui/material/Stack'
import TextField from '@mui/material/TextField'
import Typography from '@mui/material/Typography'
import { useState, type FormEvent } from 'react'
import { Navigate, useLocation, useNavigate } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import { useAuth } from '@/hooks/useAuth'

export default function LoginPage() {
  const { t } = useTranslation()
  const { login, isAuthenticated } = useAuth()
  const navigate = useNavigate()
  const location = useLocation()
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState(false)
  const [submitting, setSubmitting] = useState(false)

  const from = (location.state as { from?: string } | null)?.from ?? '/concerts'

  if (isAuthenticated) {
    return <Navigate to={from} replace />
  }

  const handleSubmit = async (event: FormEvent) => {
    event.preventDefault()
    setError(false)
    setSubmitting(true)
    try {
      await login(username, password)
      void navigate(from, { replace: true })
    } catch {
      setError(true)
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <Box sx={{ display: 'flex', justifyContent: 'center', py: 8 }}>
      <Paper elevation={2} sx={{ p: 4, width: '100%', maxWidth: 400 }}>
        <Typography variant="h5" component="h1" fontWeight={700} gutterBottom>
          {t('auth.loginTitle')}
        </Typography>
        <Box component="form" onSubmit={e => void handleSubmit(e)} noValidate>
          <Stack spacing={2}>
            {error && (
              <Alert severity="error" role="alert">
                {t('auth.invalidCredentials')}
              </Alert>
            )}
            <TextField
              label={t('auth.email')}
              type="email"
              name="username"
              autoComplete="username"
              value={username}
              onChange={event => setUsername(event.target.value)}
              required
              inputProps={{ maxLength: 255 }}
            />
            <TextField
              label={t('auth.password')}
              type="password"
              name="password"
              autoComplete="current-password"
              value={password}
              onChange={event => setPassword(event.target.value)}
              required
              inputProps={{ maxLength: 128 }}
            />
            <Button type="submit" variant="contained" disabled={submitting}>
              {t('auth.submit')}
            </Button>
          </Stack>
        </Box>
      </Paper>
    </Box>
  )
}
