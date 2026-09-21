import { lazy } from 'react'
import { Route, Routes } from 'react-router-dom'
import { MainLayout } from '@/components/layout/MainLayout'
import { RequireAuth } from '@/router/RequireAuth'

const HomePage = lazy(() => import('@/pages/Home/HomePage'))
const LoginPage = lazy(() => import('@/pages/Login/LoginPage'))
const NotFoundPage = lazy(() => import('@/pages/NotFound/NotFoundPage'))
const ConcertsPage = lazy(() => import('@/pages/Concerts/ConcertsPage'))
const ConcertDetailPage = lazy(() => import('@/pages/Concerts/ConcertDetailPage'))
const ConcertFormPage = lazy(() => import('@/pages/Concerts/ConcertFormPage'))

export default function AppRouter() {
  return (
    <Routes>
      <Route element={<MainLayout />}>
        <Route path="/" element={<HomePage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route
          path="/concerts"
          element={
            <RequireAuth>
              <ConcertsPage />
            </RequireAuth>
          }
        />
        <Route
          path="/concerts/new"
          element={
            <RequireAuth>
              <ConcertFormPage />
            </RequireAuth>
          }
        />
        <Route
          path="/concerts/:id"
          element={
            <RequireAuth>
              <ConcertDetailPage />
            </RequireAuth>
          }
        />
        <Route
          path="/concerts/:id/edit"
          element={
            <RequireAuth>
              <ConcertFormPage />
            </RequireAuth>
          }
        />
        <Route path="*" element={<NotFoundPage />} />
      </Route>
      <Route path="/404" element={<NotFoundPage />} />
    </Routes>
  )
}
