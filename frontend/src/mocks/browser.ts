import { setupWorker } from 'msw/browser'
import { handlers } from './handlers'

/**
 * MSW Service Worker used for browser-based mock interception.
 *
 * Can be activated during development to mock API responses without a running
 * backend. Start it in `main.tsx` behind an env flag if needed:
 * ```ts
 * if (import.meta.env.DEV) { await worker.start() }
 * ```
 */
export const worker = setupWorker(...handlers)
