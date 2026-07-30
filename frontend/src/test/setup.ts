/// <reference types="vitest/globals" />
import '@testing-library/jest-dom'
import { server } from '../mocks/server'
import '../i18n'

// Establish API mocking before all tests
beforeAll(() => server.listen({ onUnhandledRequest: 'warn' }))

// Reset any request handlers that we may add during the tests
afterEach(() => server.resetHandlers())

// Clean up after the tests are finished
afterAll(() => server.close())
