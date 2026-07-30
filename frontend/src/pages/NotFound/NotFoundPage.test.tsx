import { describe, it, expect } from 'vitest'
import { screen } from '@testing-library/react'
import { renderWithProviders } from '@/test/utils'
import NotFoundPage from './NotFoundPage'

describe('NotFoundPage', () => {
  it('renders 404 error code', () => {
    renderWithProviders(<NotFoundPage />)
    expect(screen.getByText('404')).toBeInTheDocument()
  })

  it('renders a heading for the not found message', () => {
    renderWithProviders(<NotFoundPage />)
    expect(screen.getByRole('heading', { level: 2 })).toBeInTheDocument()
  })

  it('renders a link to go back home', () => {
    renderWithProviders(<NotFoundPage />)
    const link = screen.getByRole('link', { name: /volver al inicio/i })
    expect(link).toBeInTheDocument()
    expect(link).toHaveAttribute('href', '/')
  })
})
