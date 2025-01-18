import React, { useEffect } from 'react';
import { createRoot } from 'react-dom/client';
import { createBrowserRouter, createRoutesFromElements, Route, RouterProvider, Navigate } from 'react-router-dom';
import App from './App.jsx';
import Dashboard from './pages/dashboard/Dashboard';
import Financial from './pages/financial/Financial';
import Calendar from './pages/calendar/Calendar';
import Announcement from './pages/announcement/Announcement';
import BarChart from './pages/barChart/BarChart';
import PieChart from './pages/pieChart/PieChart';
import LineChart from './pages/lineChart/LineChart';
import Geography from './pages/geography/Geography';
import Account from './pages/account/Account';
import Information from './pages/information/Information';
import Department from './pages/department/Department';
import { useAuthStore } from './pages/login/authStore.js';
import Login from './pages/login/Login.jsx';
import ForgotPassword from './pages/login/ForgotPassword.jsx';
import ResetPassword from './pages/login/ResetPassword.jsx';
import Application from './pages/application/Application.jsx';
import Verify2fa from './pages/login/Verify2fa.jsx';
import Event from './pages/event/Event.jsx';
import { Box, CircularProgress } from '@mui/material';

const AuthInitializer = ({ children }) => {
  const { checkAuth, isCheckingAuth } = useAuthStore();

  useEffect(() => {
    checkAuth();
  }, [checkAuth]);

  if (isCheckingAuth) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '200px' }}>
        <CircularProgress />
      </Box>
    )
  }

  return children;
};

const RedirectAuthenticatedUser = ({ children }) => {
  const { isAuthenticated } = useAuthStore();
  return isAuthenticated ? <Navigate to="/" replace /> : children;
};

const ProtectedRoute = ({ children }) => {
  const { isAuthenticated } = useAuthStore();
  return isAuthenticated ? children : <Navigate to="/login" replace />;
};

const router = createBrowserRouter(
  createRoutesFromElements(
    <>
      <Route path="/login" element={
        <RedirectAuthenticatedUser>
          <Login />
        </RedirectAuthenticatedUser>
      } />
      <Route path="/verify-otp" element={
        <RedirectAuthenticatedUser>
          <Verify2fa />
        </RedirectAuthenticatedUser>
      } />
      <Route path="/forgot-password" element={
        <RedirectAuthenticatedUser>
          <ForgotPassword />
        </RedirectAuthenticatedUser>
      } />
      <Route path="/reset-password" element={
        <RedirectAuthenticatedUser>
          <ResetPassword />
        </RedirectAuthenticatedUser>
      } />

      <Route path="/" element={<ProtectedRoute><App /></ProtectedRoute>}>
        <Route index element={<Dashboard />} />
        <Route path="account" element={<Account />} />
        <Route path="information" element={<Information />} />
        <Route path="financial" element={<Financial />} />
        <Route path="department" element={<Department />} />
        <Route path="calendar" element={<Calendar />} />
        <Route path="announcement" element={<Announcement />} />
        <Route path="events" element={<Event />} />
        <Route path="application" element={<Application />} />
        <Route path="bar" element={<BarChart />} />
        <Route path="pie" element={<PieChart />} />
        <Route path="line" element={<LineChart />} />
        <Route path="geography" element={<Geography />} />
      </Route>
    </>
  )
);

// Kết nối React DOM
createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <AuthInitializer>
      <RouterProvider router={router} />
    </AuthInitializer>
  </React.StrictMode>
);
