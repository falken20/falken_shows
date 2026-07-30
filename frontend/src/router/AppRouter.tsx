import { lazy } from 'react'
import { Navigate, Route, Routes } from 'react-router-dom'
import { MainLayout } from '@/components/layout/MainLayout'

// Lazy-loaded pages
const HomePage = lazy(() => import('@/pages/Home/HomePage'))
const NotFoundPage = lazy(() => import('@/pages/NotFound/NotFoundPage'))

export default function AppRouter() {
  return (
    <Routes>
      <Route element={<MainLayout />}>
        <Route path="/" element={<HomePage />} />
        <Route path="*" element={<NotFoundPage />} />
      </Route>
      <Route path="/404" element={<Navigate to="/" replace />} />
    </Routes>
  )
}
