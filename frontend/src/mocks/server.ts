import { setupServer } from 'msw/node'
import { handlers } from './handlers'

/**
 * MSW Node.js server used by Vitest to intercept HTTP requests in tests.
 *
 * Started in `src/test/setup.ts` before all tests and reset after each test
 * to prevent handler state leaking between cases.
 */
export const server = setupServer(...handlers)
