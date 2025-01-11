import { create } from 'zustand';
import axios from 'axios';
import qs from 'qs';

const API_URL = "http://127.0.0.1:8000/api";

axios.defaults.withCredentials = true;

export const useAuthStore = create((set) => ({
    user: null,
    isAuthenticated: false,
    error: null,
    isLoading: false,
    isCheckingAuth: true,
    message: null,
    token: null,

    login: async (username, password) => {
        set({ isLoading: true, error: null });
        try {
            
            const response = await axios.post(
                `${API_URL}/login`,
                qs.stringify({ username, password }),
                { headers: { 'Content-Type': 'application/x-www-form-urlencoded' } }
            );
            
            set({ 
                token: response.data.access_token, 
                isAuthenticated: true, 
                isLoading: false, 
                error: null, 
                user: response.data.user
            });

            const socket = new WebSocket("ws://127.0.0.1:8000/ws/" + username);
            socket.onopen = () => {
                console.log(`User ${username} is active`);
            };
            socket.onerror = (err) => {
                console.error("WebSocket error:", err);
            };

        } catch (error) {
            set({ error: error.response?.data?.message || "Error logging in", isLoading: false });
            throw error;
        }
    },

    logout: async () => {
        set({ isLoading: true, error: null });
        try {
            const socket = useAuthStore.getState().socket;
            if (socket) {
                socket.close();
            }
            set({
                user: null,
                isAuthenticated: false,
                token: null,
                message: "Logged out successfully",
                isLoading: false,
            });
        } catch (error) {
            set({ isLoading: false, error: "Error logging out" });
            throw error;
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
                    username: username,
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
