import userEvent from '@testing-library/user-event'
import { renderWithProviders, screen, waitFor } from '@/test/utils'
import ConcertsPage from './ConcertsPage'

it('renders concerts returned by the API', async () => {
  renderWithProviders(<ConcertsPage />)

  expect(await screen.findByText('Mock Concert')).toBeInTheDocument()
  expect(screen.getByText('Mock Artist')).toBeInTheDocument()
  expect(screen.getByText('Mock Venue, Madrid')).toBeInTheDocument()
})

it('navigates to detail when the concert link is activated', async () => {
  window.history.pushState({}, '', '/concerts')
  const user = userEvent.setup()
  renderWithProviders(<ConcertsPage />)

  await user.click(await screen.findByRole('link', { name: 'Mock Concert' }))

  await waitFor(() => expect(window.location.pathname).toBe('/concerts/1'))
})
