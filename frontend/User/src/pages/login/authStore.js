import { create } from 'zustand';
import axios from 'axios';
import qs from 'qs';

const API_URL = "http://52.184.86.56:8000/api";

axios.defaults.withCredentials = true;

// Helper to set default authorization header
const setAuthHeader = (token) => {
  if (token) {
    axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
  } else {
    delete axios.defaults.headers.common['Authorization'];
  }
};

export const useAuthStore = create((set) => ({
    user: null,
    isAuthenticated: false,
    error: null,
    isLoading: false,
    isCheckingAuth: true,
    message: null,
    token: null,
    userName: '',  // Add userName state

    // Add function to update userName
    setUserName: (name) => set({ userName: name }),

    login: async (username, password) => {
        set({ isLoading: true, error: null });
        try {
            const response = await axios.post(
                `${API_URL}/login`,
                qs.stringify({ username, password }),
                { headers: { 'Content-Type': 'application/x-www-form-urlencoded', } }
            );
            
            const token = response.data.access_token;
            
            // Store token in localStorage with expiration
            localStorage.setItem('token', token);
            localStorage.setItem('tokenExpiration', new Date().getTime() + 8 * 60 * 60 * 1000); // 8 hours
            
            // Set axios default header
            setAuthHeader(token);

            // Initialize user session
            await useAuthStore.getState().initializeSession(token);
            
        } catch (error) {
            set({ error: error.response?.data?.message || "Error logging in", isLoading: false });
            throw error;
        }
    },

    initializeSession: async (token) => {
        try {
            // Set auth header
            setAuthHeader(token);
            
            // Fetch user data including name
            const response = await axios.get(`${API_URL}/me/personal_info`, {
                headers: { Authorization: `Bearer ${token}` }
            });
            
            set({ 
                token,
                isAuthenticated: true,
                isLoading: false,
                error: null,
                isCheckingAuth: false,
                userName: response.data.fullname || '' // Set initial userName
            });
        } catch (error) {
            set({ isCheckingAuth: false, isLoading: false });
            useAuthStore.getState().logout();
        }
    },

    logout: () => {
        localStorage.removeItem('token');
        localStorage.removeItem('tokenExpiration');
        setAuthHeader(null);
        set({ 
            user: null, 
            isAuthenticated: false, 
            token: null,
            isCheckingAuth: false,
            userName: '' // Clear userName on logout
        });
    },

    checkAuth: async () => {
        set({ isCheckingAuth: true });
        
        const token = localStorage.getItem('token');
        const expiration = localStorage.getItem('tokenExpiration');
        
        if (!token || !expiration) {
            set({ isCheckingAuth: false, isAuthenticated: false });
            return false;
        }

        // Check if token is expired
        if (new Date().getTime() > parseInt(expiration)) {
            useAuthStore.getState().logout();
            set({ isCheckingAuth: false });
            return false;
        }

        try {
            // Initialize session with existing token
            await useAuthStore.getState().initializeSession(token);
            return true;
        } catch (error) {
            useAuthStore.getState().logout();
            set({ isCheckingAuth: false });
            return false;
        }
    },

    forgotPassword: async (username) => {
        set({ isLoading: true, error: null });
        try {
            const response = await axios.post(`${API_URL}/forgot-password`, null, {
                params: { username },
            });
            set({ message: response.data.message, isLoading: false });
        } catch (error) {
            set({
                isLoading: false,
                error: error.response.data.message || "Error sending reset password email",
            });
            throw error;
        }
    },

    resetPassword: async (username, otpCode, newPassword, confirmPassword) => {
        set({ isLoading: true, error: null })
        try {
            const response = await axios.post(`${API_URL}/reset-password`, null, {
                params: {
                    username,
                    otp_code: otpCode,
                    new_password: newPassword,
                    confirm_password: confirmPassword
                }
            });
            set({ message: response.data.message, isLoading: false })
        } catch (error) {
            set({
                isLoading: false,
                error: error.response.data.message || "Error resetting password"
            })
            throw error
        }
    }
}));

// Set up axios interceptor for automatic token handling
axios.interceptors.response.use(
    response => response,
    error => {
        if (error.response?.status === 401) {
            useAuthStore.getState().logout();
        }
        return Promise.reject(error);
    }
);