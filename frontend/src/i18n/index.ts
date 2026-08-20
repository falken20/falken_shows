import i18n from 'i18next'
import { initReactI18next } from 'react-i18next'
import LanguageDetector from 'i18next-browser-languagedetector'
import es from './locales/es.json'
import en from './locales/en.json'

/**
 * i18next instance configured for the application.
 *
 * - Supported languages: `es` (Spanish – default) and `en` (English).
 * - Language detection uses the browser's `navigator.language` via
 *   `i18next-browser-languagedetector`, falling back to `'es'`.
 * - `escapeValue: false` is safe because React escapes values in JSX.
 * - `debug: true` is enabled in Vite dev mode to log missing keys to console.
 *
 * To add a new language:
 * 1. Create `src/i18n/locales/<lang>.json` with translated strings.
 * 2. Import it here and add an entry to `resources`.
 */
void i18n
  .use(LanguageDetector)
  .use(initReactI18next)
  .init({
    resources: {
      es: { translation: es },
      en: { translation: en },
    },
    fallbackLng: 'es',
    lng: 'es',
    debug: import.meta.env.DEV,
    interpolation: {
      escapeValue: false,
    },
  })

export default i18n
