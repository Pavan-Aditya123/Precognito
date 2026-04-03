import '@testing-library/jest-dom'
import { vi } from 'vitest'

// Mock next/navigation
vi.mock('next/navigation', () => ({
  usePathname: () => '/',
  useRouter: () => ({
    push: vi.fn(),
    replace: vi.fn(),
    prefetch: vi.fn(),
  }),
}))

// Mock better-auth client
vi.mock('@/lib/auth-client', () => ({
  useSession: () => ({
    data: {
      user: {
        id: '1',
        name: 'Test User',
        email: 'test@example.com',
        role: 'ADMIN',
      },
    },
    isPending: false,
  }),
  signOut: vi.fn(),
  signIn: {
    email: vi.fn(),
  },
  authClient: {
    signUp: {
      email: vi.fn(),
    },
  },
}))
