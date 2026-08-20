import { lazy } from 'react'
import { Navigate, Route, Routes } from 'react-router-dom'
import { MainLayout } from '@/components/layout/MainLayout'

// Lazy-load pages so each route's bundle is only fetched when first visited.
const HomePage = lazy(() => import('@/pages/Home/HomePage'))
const NotFoundPage = lazy(() => import('@/pages/NotFound/NotFoundPage'))
const ConcertsPage = lazy(() => import('@/pages/Concerts/ConcertsPage'))
const ConcertDetailPage = lazy(() => import('@/pages/Concerts/ConcertDetailPage'))
const ConcertFormPage = lazy(() => import('@/pages/Concerts/ConcertFormPage'))

/**
 * Declarative route tree for the application.
 *
 * All routes that should share the persistent navigation shell (TopBar) are
 * nested inside the `<MainLayout>` route.  Add new pages following this pattern:
 *
 * ```tsx
 * const ConcertsPage = lazy(() => import('@/pages/Concerts/ConcertsPage'))
 * // Inside the MainLayout Route:
 * <Route path="/concerts" element={<ConcertsPage />} />
 * ```
 *
 * Then register the page in `AppRouter` and add navigation in {@link TopBar}.
 */
export default function AppRouter() {
  return (
    <Routes>
      <Route element={<MainLayout />}>
        <Route path="/" element={<HomePage />} />
        <Route path="/concerts" element={<ConcertsPage />} />
        <Route path="/concerts/new" element={<ConcertFormPage />} />
        <Route path="/concerts/:id" element={<ConcertDetailPage />} />
        <Route path="/concerts/:id/edit" element={<ConcertFormPage />} />
        <Route path="*" element={<NotFoundPage />} />
      </Route>
      <Route path="/404" element={<Navigate to="/" replace />} />
    </Routes>
  )
}
