import { expect, test } from '@playwright/test'

const concert = {
  id: 1,
  title: 'E2E Concert',
  artist: {
    id: 1,
    name: 'E2E Artist',
    bio: null,
    country: 'ES',
    created_at: '2024-01-01T00:00:00Z',
  },
  venue: {
    id: 1,
    name: 'E2E Venue',
    city: 'Madrid',
    country: 'ES',
    capacity: 500,
    created_at: '2024-01-01T00:00:00Z',
  },
  date: '2024-06-15T20:00:00Z',
  setlist: ['Intro'],
  notes: 'E2E notes',
  rating: 5,
  ticket_price: 30,
  currency: 'EUR',
  created_at: '2024-01-01T00:00:00Z',
  updated_at: '2024-01-01T00:00:00Z',
}

test('concert list navigates to detail', async ({ page }) => {
  await page.route('**/api/v1/concerts?page=1&page_size=20', async route => {
    await route.fulfill({
      json: { items: [concert], total: 1, page: 1, page_size: 20, pages: 1 },
    })
  })
  await page.route('**/api/v1/concerts/1', async route => {
    await route.fulfill({ json: concert })
  })

  await page.goto('/concerts')
  await expect(page.getByRole('heading', { name: 'Conciertos' })).toBeVisible()
  await expect(page.getByText('E2E Concert')).toBeVisible()

  await page.getByRole('link', { name: 'E2E Concert' }).click()
  await expect(page).toHaveURL(/\/concerts\/1$/)
  await expect(page.getByRole('heading', { name: 'E2E Concert' })).toBeVisible()
  await expect(page.getByText('E2E notes')).toBeVisible()
})
