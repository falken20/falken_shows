import Box from '@mui/material/Box'
import { Outlet } from 'react-router-dom'
import { TopBar } from './TopBar'

/**
 * Persistent application shell shared by all main routes.
 *
 * Renders the sticky {@link TopBar} at the top and fills the remaining
 * viewport height with the current page content via React Router's `<Outlet>`.
 * Responsive horizontal padding is applied via MUI's `sx` breakpoint syntax.
 */
export function MainLayout() {
  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
      <TopBar />
      <Box component="main" sx={{ flexGrow: 1, p: { xs: 2, md: 3 } }}>
        <Outlet />
      </Box>
    </Box>
  )
}
