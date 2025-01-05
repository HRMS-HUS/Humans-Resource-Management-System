import Sheet from '@mui/joy/Sheet';
import Typography from '@mui/joy/Typography';
import FormControl from '@mui/joy/FormControl';
import FormLabel from '@mui/joy/FormLabel';
import Input from '@mui/joy/Input';
import LoadingButton from '@mui/lab/LoadingButton';
import { Box, Snackbar, Alert } from '@mui/material';
import { useState } from 'react';
import { useAuthStore } from './authStore';
import { useNavigate } from 'react-router-dom';

const ResetPassword = () => {

    const navigate = useNavigate()
    const [username, setUsername] = useState("")
    const [otp, setOtp] = useState("")
    const [newPassword, setNewPassword] = useState("")
    const [confirmPassword, setConfirmPassword] = useState("")
    const { isLoading, resetPassword } = useAuthStore()
    const [openSnackbar, setOpenSnackbar] = useState(false);
    const [snackbarMessage, setSnackbarMessage] = useState("");

    const handleSubmit = async (e) => {
        e.preventDefault()

        if (newPassword !== confirmPassword) {
            alert("Passwords do not match")
            return
        }

        try {
            await resetPassword(username, otp, newPassword, confirmPassword);
            setSnackbarMessage("Password reset successfully! Redirecting to login...");
            setOpenSnackbar(true);
            setTimeout(() => {
                navigate("/login")
            }, 3000);
        } catch (error) {
            console.error(error);
            setSnackbarMessage("An error occurred. Please try again.");
            setOpenSnackbar(true);
        }
    }

    const handleCloseSnackbar = () => {
        setOpenSnackbar(false);
    };

    return (
        <main style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh', margin: 0, backgroundImage: 'url("https://images4.alphacoders.com/211/thumb-1920-211006.jpg")', backgroundSize: 'cover', backgroundPosition: 'center', }}>
            <Sheet sx={{ width: 430, mx: 'auto', my: 4, py: 3, px: 2, display: 'flex', flexDirection: 'column', gap: 2, borderRadius: 'sm', boxShadow: 'md', background: 'transparent', backgroundColor: 'rgba(128, 128, 128, 0.6)' }} variant="outlined">
                <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', height: '28vh', textAlign: 'center', }}>
                    <img src={'https://cdnlogo.com/logos/n/71/nvidia.svg'} style={{ width: 120, height: 120 }} />
                    <Typography level="h2" component="h1"><b>Reset Password</b></Typography>
                    <Typography>Please enter the OTP code and the new password you want to reset.</Typography>
                </Box>
                <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
                    <FormControl>
                        <FormLabel sx={{ fontSize: '16px' }}>Username</FormLabel>
                        <Input name="username" type="text" placeholder="Username" sx={{ height: '42px', backgroundColor: 'rgba(128, 128, 128, 0.6)' }} onChange={(e) => setUsername(e.target.value)} />
                    </FormControl>
                    <FormControl>
                        <FormLabel sx={{ fontSize: '16px' }}>OTP Code</FormLabel>
                        <Input name="otp" type="text" placeholder="OTP Code" sx={{ height: '42px', backgroundColor: 'rgba(128, 128, 128, 0.6)' }} onChange={(e) => setOtp(e.target.value)} />
                    </FormControl>
                    <Box style={{ display: 'flex', gap: '16px' }}>
                        <FormControl style={{ flex: 1 }}>
                            <FormLabel sx={{ fontSize: '16px' }}>New Password</FormLabel>
                            <Input name="new_password" type="password" placeholder="New Password" sx={{ height: '42px', backgroundColor: 'rgba(128, 128, 128, 0.6)' }} onChange={(e) => setNewPassword(e.target.value)} />
                        </FormControl>
                        <FormControl style={{ flex: 1 }}>
                            <FormLabel sx={{ fontSize: '16px' }}>Confirm Password</FormLabel>
                            <Input name="confirm_password" type="password" placeholder="Confirm Password" sx={{ height: '42px', backgroundColor: 'rgba(128, 128, 128, 0.6)' }} onChange={(e) => setConfirmPassword(e.target.value)} />
                        </FormControl>
                    </Box>
                    <LoadingButton
                        type="submit"
                        loading={isLoading}
                        disabled={isLoading}
                        sx={{
                            backgroundColor: '#1976d2',
                            color: 'white',
                            '&:hover': { backgroundColor: '#115293', transform: 'scale(1.02)', },
                            '&:active': { transform: 'scale(0.98)', },
                            marginTop: '12px',
                            height: '48px',
                        }}
                    >
                        Reset Password
                    </LoadingButton>
                </form>
            </Sheet>
            <Snackbar
                open={openSnackbar}
                autoHideDuration={4000}
                onClose={handleCloseSnackbar}
                anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
            >
                <Alert onClose={handleCloseSnackbar} severity={snackbarMessage.includes("successfully") ? "success" : "error"} sx={{ width: '100%' }}>
                    {snackbarMessage}
                </Alert>
            </Snackbar>
        </main>
    )
}

export default ResetPassword
