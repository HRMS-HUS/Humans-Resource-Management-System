import { create } from 'zustand';
import axios from 'axios';
import qs from 'qs';

const API_URL = "http://52.184.86.56:8000/api";

axios.defaults.withCredentials = true;

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
    username: null,
    email: null,

    checkAuth: () => {
        const token = localStorage.getItem('token');
        const tokenExpiration = localStorage.getItem('tokenExpiration');

        if (token && tokenExpiration && new Date().getTime() < parseInt(tokenExpiration)) {
            setAuthHeader(token);
            set({ isAuthenticated: true, token, isCheckingAuth: false });
        } else {
            localStorage.removeItem('token');
            localStorage.removeItem('tokenExpiration');
            setAuthHeader(null);
            set({ isAuthenticated: false, token: null, isCheckingAuth: false });
        }
    },

    login: async (username, password) => {
        set({ isLoading: true, error: null });
        try {
            const response = await axios.post(
                `${API_URL}/login/admin`,
                qs.stringify({ username, password }),
                { headers: { 'Content-Type': 'application/x-www-form-urlencoded' } }
            );

            set({
                isLoading: false,
                error: null,
                username: username
            });

        } catch (error) {
            set({ error: error.response?.data?.message || "Error logging in", isLoading: false });
            throw error;
        }
    },

    verify2fa: async (username, otp) => {
        set({ isLoading: true, error: null });
        try {
            const response = await axios.post(
                `${API_URL}/verify-otp`,
                null,
                { params: { username: username, otp_code: otp } }
            );

            const token = response.data.access_token;

            const tokenExpiration = new Date().getTime() + 8 * 60 * 60 * 1000;
            localStorage.setItem('token', token);
            localStorage.setItem('tokenExpiration', tokenExpiration.toString());

            setAuthHeader(token);
            set({
                isAuthenticated: true,
                isLoading: false,
                error: null,
                username: null,
                token: token
            });

        } catch (error) {
            set({
                isLoading: false,
                error: error.response?.data?.message || "Error verifying OTP",
            });
            throw error;
        }
    },

    logout: async () => {
        set({ isLoading: true, error: null });
        try {
            await axios.post(
                `${API_URL}/logout/admin`,
                null,
                { headers: { Authorization: `Bearer ${localStorage.getItem('token')}`, }, }
            );

            localStorage.removeItem('token');
            localStorage.removeItem('tokenExpiration');
            setAuthHeader(null);

            set({
                isAuthenticated: false,
                user: null,
                token: null,
                isLoading: false
            });
        } catch (error) {
            set({
                error: error.response?.data?.message || "Error during logout",
                isLoading: false,
            });
            throw error;
        }
    },

    forgotPassword: async (email) => {
        set({ isLoading: true, error: null });
        try {
            const response = await axios.post(`${API_URL}/forgot-password`, null, {
                params: { email },
            });
            set({ message: response.data.message, isLoading: false, email: email });
        } catch (error) {
            set({
                isLoading: false,
                error: error.response.data.message || "Error sending reset password email",
            });
            throw error;
        }
    },

    resetPassword: async (email, otpCode, newPassword, confirmPassword) => {
        set({ isLoading: true, error: null });
        try {
            const response = await axios.post(`${API_URL}/reset-password`, null, {
                params: {
                    email: email,
                    otp_code: otpCode,
                    new_password: newPassword,
                    confirm_password: confirmPassword
                }
            });
            set({ message: response.data.message, isLoading: false, email: null });
        } catch (error) {
            set({
                isLoading: false,
                error: error.response.data.message || "Error resetting password"
            });
            throw error;
        }
    }
}));
