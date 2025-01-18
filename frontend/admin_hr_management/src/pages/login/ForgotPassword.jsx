import { TextField, Button, Box, Snackbar, Alert, Typography, FormControl, FormLabel } from '@mui/material';
import ArrowCircleLeftIcon from '@mui/icons-material/ArrowCircleLeft';
import CircularProgress from '@mui/material/CircularProgress';
import { useState } from 'react';
import { useAuthStore } from './authStore';
import { useNavigate } from 'react-router-dom';

const ForgotPassword = () => {

    const navigate = useNavigate();
    const [email, setEmail] = useState("");
    const { isLoading, forgotPassword } = useAuthStore();
    const [openSnackbar, setOpenSnackbar] = useState(false);
    const [snackbarMessage, setSnackbarMessage] = useState("");

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            await forgotPassword(email);
            setSnackbarMessage("OTP code has been sent to your email.");
            setOpenSnackbar(true);
            setTimeout(() => {
                navigate("/reset-password");
            }, 3000);
        } catch (error) {
            console.error(error);
            setSnackbarMessage("An error occurred. Please try again.");
            setOpenSnackbar(true);
        }
    };

    const handleCloseSnackbar = () => {
        setOpenSnackbar(false);
    };

    return (
        <main style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh', margin: 0, backgroundImage: 'url("https://vti-solutions.vn/wp-content/uploads/2022/09/xu-huong-quan-tri-nhan-su.png")', backgroundSize: 'cover', backgroundPosition: 'center', }}>
            <Box sx={{ width: 370, mx: 'auto', my: 4, py: 3, px: 2, display: 'flex', flexDirection: 'column', gap: 3, borderRadius: 2, boxShadow: 3, backgroundColor: 'rgba(128, 128, 128, 0.9)', border: '0.5px solid #b2ebf2' }}>
                <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', height: '28vh', textAlign: 'center', mt: 5, gap: 2 }}>
                    <img src={'https://cdn.haitrieu.com/wp-content/uploads/2021/12/hai-trieu-favicon.png'} style={{ width: 120, height: 120 }} />
                    <Typography variant="h4" gutterBottom sx={{ fontSize: '30px', color: 'rgba(0, 0, 0, 0.7)' }}><b>Welcome to Company!</b></Typography>
                    <Typography sx={{ color: 'rgba(0, 0, 0, 0.7)' }}>Enter your email and we'll send you a link to reset your password.</Typography>
                </Box>
                <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
                    <FormControl fullWidth>
                        <FormLabel sx={{ fontSize: '15px', color: 'rgba(0, 0, 0, 0.6)', fontWeight: 'bold', mb: 0.5, }}>
                            Email
                        </FormLabel>
                        <TextField
                            placeholder="Email"
                            variant="outlined"
                            fullWidth
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            InputProps={{
                                sx: {
                                    backgroundColor: '#f5f5f5',
                                    height: '43px',
                                    display: 'flex',
                                    alignItems: 'center',
                                    padding: '0 14px',
                                    '&:hover': { backgroundColor: '#f5f5f5', },
                                    '&.Mui-focused': { backgroundColor: '#f5f5f5', },
                                },
                            }}
                            sx={{
                                '& .MuiOutlinedInput-root': {
                                    '& fieldset': { borderColor: '#b2ebf2', },
                                    '&:hover fieldset': { borderColor: '#80deea', },
                                    '&.Mui-focused fieldset': { borderColor: '#2e86c1', boxShadow: '0 0 5px rgba(46, 134, 193, 0.5)', },
                                    height: '43px'
                                },
                                '& .MuiInputBase-input': { height: '100%', padding: '0', lineHeight: '50px', fontSize: '16px', },
                            }}
                        />
                    </FormControl>
                    <Button
                        type="submit"
                        variant="contained"
                        color="primary"
                        disabled={isLoading}
                        sx={{ marginTop: '12px', height: '48px', fontWeight: 'bold' }}
                    >
                        {isLoading ? <CircularProgress size={24} color="inherit" /> : 'Send OTP Code'}
                    </Button>
                </form>
                <Button
                    onClick={() => navigate('/login')}
                    startIcon={<ArrowCircleLeftIcon />}
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
                    }}
                >
                    Back to Login
                </Button>
            </Box>
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
    );
};

export default ForgotPassword;
