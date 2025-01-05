import React from 'react';
import { createRoot } from 'react-dom/client';
import { createBrowserRouter, createRoutesFromElements, Route, RouterProvider, Navigate } from 'react-router-dom';
import { CssVarsProvider } from '@mui/joy/styles';
import App from './App.jsx';
import Dashboard from './pages/dashboard/Dashboard';
import Financial from './pages/financial/Financial';
import Form from './pages/form/Form';
import Calendar from './pages/calendar/Calendar';
import FAQ from './pages/faq/Faq';
import BarChart from './pages/barChart/BarChart';
import PieChart from './pages/pieChart/PieChart';
import LineChart from './pages/lineChart/LineChart';
import Geography from './pages/geography/Geography';
import Account from './pages/account/Account';
import Information from './pages/information/Information';
import Department from './pages/department/Department';
import { useAuthStore } from './pages/login/authStore.js';
import Login from './pages/login/Login.jsx';

const RedirectAuthenticatedUser = ({ children }) => {
  const { isAuthenticated } = useAuthStore()
  if (isAuthenticated) {
    return <Navigate to='/' replace />
  }
  return children
}

const ProtectedRoute = ({ children }) => {
  const { isAuthenticated } = useAuthStore()
  if (!isAuthenticated) {
    return <Navigate to='/login' replace />
  }
  return children
}

const router = createBrowserRouter(
  createRoutesFromElements(
    <>
      <Route path="/login" element={
        <RedirectAuthenticatedUser>
          <Login />
        </RedirectAuthenticatedUser>
      } />
      <Route path="/" element={<ProtectedRoute><App /></ProtectedRoute>}>
        <Route index element={<Dashboard />} />
        <Route path="account" element={<Account />} />
        <Route path="information" element={<Information />} />
        <Route path="financial" element={<Financial />} />
        <Route path="department" element={<Department />} />
        <Route path="form" element={<Form />} />
        <Route path="calendar" element={<Calendar />} />
        <Route path="faq" element={<FAQ />} />
        <Route path="bar" element={<BarChart />} />
        <Route path="pie" element={<PieChart />} />
        <Route path="line" element={<LineChart />} />
        <Route path="geography" element={<Geography />} />
      </Route>
    </>
  )
);

createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <CssVarsProvider>
      <RouterProvider router={router} />
    </CssVarsProvider>
  </React.StrictMode>
);
