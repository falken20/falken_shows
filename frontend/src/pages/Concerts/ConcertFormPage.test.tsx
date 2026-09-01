import userEvent from '@testing-library/user-event'
import { renderWithProviders, screen, waitFor } from '@/test/utils'
import { Route, Routes } from 'react-router-dom'
import ConcertFormPage from './ConcertFormPage'

beforeEach(() => {
  localStorage.setItem('live-memories-token', 'mock-jwt-token')
})

afterEach(() => {
  localStorage.clear()
})

it('validates required fields', async () => {
  const user = userEvent.setup()
  window.history.pushState({}, '', '/concerts/new')

  renderWithProviders(
    <Routes>
      <Route path="/concerts/new" element={<ConcertFormPage />} />
    </Routes>
  )

  await user.click(screen.getByRole('button', { name: 'Guardar' }))

  expect(await screen.findAllByText('Este campo es obligatorio')).toHaveLength(2)
})

it('creates a concert and navigates to the detail page', async () => {
  const user = userEvent.setup()
  window.history.pushState({}, '', '/concerts/new')

  renderWithProviders(
    <Routes>
      <Route path="/concerts/new" element={<ConcertFormPage />} />
      <Route path="/concerts/:id" element={<div>detail</div>} />
    </Routes>
  )

  await user.type(screen.getByLabelText(/Título/), 'New Mock Concert')
  await user.type(screen.getByLabelText(/Fecha/), '2024-06-15')
  await user.clear(screen.getByLabelText(/Moneda/))
  await user.type(screen.getByLabelText(/Moneda/), 'EUR')
  await user.click(screen.getByRole('button', { name: 'Guardar' }))

  await waitFor(() => expect(window.location.pathname).toBe('/concerts/2'))
})

it('redirects invalid edit route params to 404', () => {
  window.history.pushState({}, '', '/concerts/not-a-number/edit')

  renderWithProviders(
    <Routes>
      <Route path="/concerts/:id/edit" element={<ConcertFormPage />} />
      <Route path="/404" element={<div>404</div>} />
    </Routes>
  )

  expect(window.location.pathname).toBe('/404')
})
