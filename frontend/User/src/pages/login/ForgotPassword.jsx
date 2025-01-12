import Sheet from '@mui/joy/Sheet';
import Typography from '@mui/joy/Typography';
import FormControl from '@mui/joy/FormControl';
import FormLabel from '@mui/joy/FormLabel';
import Input from '@mui/joy/Input';
import ArrowCircleLeftIcon from '@mui/icons-material/ArrowCircleLeft';
import LoadingButton from '@mui/lab/LoadingButton';
import Link from '@mui/joy/Link';
import { Box, Snackbar, Alert } from '@mui/material';
import { useState } from 'react';
import { useAuthStore } from './authStore';
import { useNavigate } from 'react-router-dom';

const ForgotPassword = () => {

    const navigate = useNavigate()
    const [username, setUsername] = useState("")
    const { isLoading, forgotPassword } = useAuthStore()
    const [openSnackbar, setOpenSnackbar] = useState(false);
    const [snackbarMessage, setSnackbarMessage] = useState("");

    const handleSubmit = async (e) => {
        e.preventDefault()
        try {
            await forgotPassword(username)
            setSnackbarMessage("OTP code has been sent to your email.");
            setOpenSnackbar(true);
            setTimeout(() => {
                navigate("/reset-password")
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
            <Sheet sx={{ width: 370, mx: 'auto', my: 4, py: 3, px: 2, display: 'flex', flexDirection: 'column', gap: 2, borderRadius: 'sm', boxShadow: 'md', background: 'transparent', backgroundColor: 'rgba(128, 128, 128, 0.6)' }} variant="outlined">
                <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', height: '28vh', textAlign: 'center', }}>
                    <img src={'https://cdnlogo.com/logos/n/71/nvidia.svg'} style={{ width: 120, height: 120 }} />
                    <Typography level="h2" component="h1"><b>Forgot Password</b></Typography>
                    <Typography>Enter your username and we'll send you a link to reset your password.</Typography>
                </Box>
                <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
                    <FormControl>
                        <FormLabel sx={{ fontSize: '16px' }}>Username</FormLabel>
                        <Input name="username" type="text" placeholder="Username" sx={{ height: '42px', backgroundColor: 'rgba(128, 128, 128, 0.6)' }} onChange={(e) => setUsername(e.target.value)} />
                    </FormControl>
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
                        Send OTP Code
                    </LoadingButton>
                </form>
                <Link
                    href="/login"
                    sx={{
                        display: 'flex',
                        alignItems: 'center',
                        color: '#2196F3',
                        textDecoration: 'none',
                        fontWeight: '500',
                        '&:hover': {
                            color: '#1976D2',
                            transform: 'translateX(-5px)',
                            transition: 'transform 0.3s ease, color 0.3s ease',
                        },
                        gap: 1,
                    }}
                >
                    <ArrowCircleLeftIcon sx={{ fontSize: 24 }} />
                    Back to Login
                </Link>
            </Sheet>
            <Snackbar
                open={openSnackbar}
                autoHideDuration={4000}
                onClose={handleCloseSnackbar}
                anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
            >
                <Alert onClose={handleCloseSnackbar} severity={snackbarMessage.includes("OTP") ? "success" : "error"} sx={{ width: '100%' }}>
                    {snackbarMessage}
                </Alert>
            </Snackbar>
        </main>
    )
}

export default ForgotPassword
