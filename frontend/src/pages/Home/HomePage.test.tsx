import { describe, it, expect } from 'vitest'
import { screen, waitFor } from '@testing-library/react'
import { renderWithProviders } from '@/test/utils'
import HomePage from './HomePage'

describe('HomePage', () => {
  it('renders the app title', () => {
    renderWithProviders(<HomePage />)
    expect(screen.getByRole('heading', { level: 1 })).toBeInTheDocument()
  })

  it('renders the API status section', () => {
    renderWithProviders(<HomePage />)
    expect(screen.getByLabelText('Estado de la API')).toBeInTheDocument()
  })

  it('shows loading state initially', () => {
    renderWithProviders(<HomePage />)
    expect(screen.getByText('Cargando...')).toBeInTheDocument()
  })

  it('shows API health status after loading', async () => {
    renderWithProviders(<HomePage />)
    await waitFor(() => {
      expect(screen.getByText('OK')).toBeInTheDocument()
    })
  })

  it('shows app version information', async () => {
    renderWithProviders(<HomePage />)
    await waitFor(() => {
      expect(screen.getByText(/v0\.1\.0/i)).toBeInTheDocument()
    })
  })
})
