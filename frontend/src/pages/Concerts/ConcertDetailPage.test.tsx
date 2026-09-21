import { renderWithProviders, screen } from '@/test/utils'
import { Route, Routes } from 'react-router-dom'
import ConcertDetailPage from './ConcertDetailPage'

beforeEach(() => {
  sessionStorage.setItem('live-memories-token', 'mock-jwt-token')
})

afterEach(() => {
  sessionStorage.clear()
})

it('renders concert details returned by the API', async () => {
  window.history.pushState({}, '', '/concerts/1')

  renderWithProviders(
    <Routes>
      <Route path="/concerts/:id" element={<ConcertDetailPage />} />
    </Routes>
  )

  expect(await screen.findByRole('heading', { name: 'Mock Concert' })).toBeInTheDocument()
  expect(screen.getByText('Mock Artist')).toBeInTheDocument()
  expect(screen.getByText('Mock Venue, Madrid')).toBeInTheDocument()
  expect(screen.getByText('Great show')).toBeInTheDocument()
  expect(screen.getByText('1. Song 1')).toBeInTheDocument()
})

it('redirects invalid route params to 404', () => {
  window.history.pushState({}, '', '/concerts/not-a-number')

  renderWithProviders(
    <Routes>
      <Route path="/concerts/:id" element={<ConcertDetailPage />} />
      <Route path="/404" element={<div>404</div>} />
    </Routes>
  )

  expect(window.location.pathname).toBe('/404')
})
