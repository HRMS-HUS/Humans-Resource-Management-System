import { Routes, Route, Navigate } from 'react-router-dom';
import { ThemeProvider } from './context/ThemeContext';
import Layout from './components/Layout';
import Dashboard from './pages/Dashboard';
import Attendance from './pages/Attendance';
import Schedule from './pages/Schedule';
import Salary from './pages/Salary';
import { useAuthStore } from './pages/login/authStore.js';
import Login from './pages/login/Login.jsx';
import ForgotPassword from './pages/login/ForgotPassword.jsx';
import ResetPassword from './pages/login/ResetPassword.jsx';
import { useEffect } from 'react';
import CircularProgress from '@mui/joy/CircularProgress';

// Component to redirect authenticated users away from auth pages
const RedirectAuthenticatedUser = ({ children }) => {
  const { isAuthenticated, isCheckingAuth } = useAuthStore();
  
  if (isCheckingAuth) {
    return <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>
      <CircularProgress />
    </div>;
  }
  
  if (isAuthenticated) {
    return <Navigate to="/" replace />;
  }
  
  return children;
};

// Component to protect routes that require authentication
const ProtectedRoute = ({ children }) => {
  const { isAuthenticated, isCheckingAuth, checkAuth } = useAuthStore();

  useEffect(() => {
    checkAuth();
  }, []);

  if (isCheckingAuth) {
    return <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>
      <CircularProgress />
    </div>;
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  return children;
};
axios.interceptors.response.use(
  response => response,
  error => {
    if (error.response?.status === 401) {
      useAuthStore.getState().logout();
    }
    return Promise.reject(error);
  }
);
function App() {
  const { checkAuth } = useAuthStore();

  useEffect(() => {
    checkAuth();
  }, []);

  return (
    <ThemeProvider>
      <Routes>
        {/* Public authentication routes */}
        <Route
          path="/login"
          element={
            <RedirectAuthenticatedUser>
              <Login />
            </RedirectAuthenticatedUser>
          }
        />
        <Route
          path="/forgot-password"
          element={
            <RedirectAuthenticatedUser>
              <ForgotPassword />
            </RedirectAuthenticatedUser>
          }
        />
        <Route
          path="/reset-password"
          element={
            <RedirectAuthenticatedUser>
              <ResetPassword />
            </RedirectAuthenticatedUser>
          }
        />

        {/* Protected routes wrapped in Layout */}
        <Route
          path="/"
          element={
            <ProtectedRoute>
              <Layout />
            </ProtectedRoute>
          }
        >
          <Route index element={<Dashboard />} />
          <Route path="/attendance" element={<Attendance />} />
          <Route path="/schedule" element={<Schedule />} />
          <Route path="/salary" element={<Salary />} />
        </Route>
      </Routes>
    </ThemeProvider>
  );
}

export default App;