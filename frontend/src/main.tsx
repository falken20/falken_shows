import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App'
import { ThemeModeProvider } from '@/hooks/useThemeMode'
import { AuthProvider } from '@/hooks/useAuth'
import './i18n'

async function enableMocking() {
  if (import.meta.env.DEV && import.meta.env.VITE_MSW_ENABLED === 'true') {
    const { worker } = await import('./mocks/browser')
    return worker.start({ onUnhandledRequest: 'warn' })
  }
}

void enableMocking().then(() => {
  ReactDOM.createRoot(document.getElementById('root')!).render(
    <React.StrictMode>
      <ThemeModeProvider>
        <AuthProvider>
          <App />
        </AuthProvider>
      </ThemeModeProvider>
    </React.StrictMode>
  )
})
