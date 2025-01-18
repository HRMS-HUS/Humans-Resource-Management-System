import { Box, Typography, TextField, Button, Link, CircularProgress, FormControl, FormLabel, Snackbar, Alert } from '@mui/material';
import ErrorIcon from '@mui/icons-material/Error';
import { useState } from 'react';
import { useAuthStore } from './authStore';
import { useNavigate } from 'react-router-dom';

const Login = () => {
    const navigate = useNavigate();
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const { login, error, isLoading } = useAuthStore();
    const [openSnackbar, setOpenSnackbar] = useState(false);
    const [snackbarMessage, setSnackbarMessage] = useState('');
    const [snackbarSeverity, setSnackbarSeverity] = useState('success');

    const handleLogin = async (e) => {
        e.preventDefault();
        try {
            await login(username, password);
            setSnackbarMessage('OTP sent to your email successfully');
            setSnackbarSeverity('success');
            setOpenSnackbar(true);
            setTimeout(() => {
                navigate('/verify-otp');
            }, 2000);
        } catch (err) {
            setSnackbarMessage(err?.response?.data?.message || 'OTP sent failed');
            setSnackbarSeverity('error');
            setOpenSnackbar(true);
        }
    };

    const handleCloseSnackbar = () => {
        setOpenSnackbar(false);
    };

    return (
        <main style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh', margin: 0, backgroundImage: 'url("https://vti-solutions.vn/wp-content/uploads/2022/09/xu-huong-quan-tri-nhan-su.png")', backgroundSize: 'cover', backgroundPosition: 'center', }}>
            <Box sx={{ width: 370, height: 490, mx: 'auto', my: 4, py: 3, px: 2, display: 'flex', flexDirection: 'column', gap: 2, borderRadius: 1, boxShadow: 3, backgroundColor: 'rgba(128, 128, 128, 0.9)', border: '0.5px solid #b2ebf2' }}>
                <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', height: '28vh', textAlign: 'center', mt: 1, gap: 2 }}>
                    <img src={'https://cdn.haitrieu.com/wp-content/uploads/2021/12/hai-trieu-favicon.png'} style={{ width: 120, height: 120 }} />
                    <Typography variant="h4" gutterBottom sx={{ fontSize: '30px', color: 'rgba(0, 0, 0, 0.7)' }}>
                        <b>Welcome to Company!</b>
                    </Typography>
                </Box>
                <form onSubmit={handleLogin} style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
                    <FormControl fullWidth>
                        <FormLabel sx={{ fontSize: '15px', color: 'rgba(0, 0, 0, 0.6)', fontWeight: 'bold', mb: 0.5, }}>
                            Username
                        </FormLabel>
                        <TextField
                            placeholder="Username"
                            variant="outlined"
                            fullWidth
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
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
                    <FormControl fullWidth>
                        <FormLabel sx={{ fontSize: '15px', color: 'rgba(0, 0, 0, 0.6)', fontWeight: 'bold', mb: 0.5, }}>
                            Password
                        </FormLabel>
                        <TextField
                            placeholder="Password"
                            variant="outlined"
                            type="password"
                            fullWidth
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            InputProps={{
                                sx: {
                                    backgroundColor: '#f5f5f5',
                                    height: '43px',
                                },
                            }}
                            sx={{
                                '& .MuiOutlinedInput-root': {
                                    '& fieldset': { borderColor: '#b2ebf2', },
                                    '&:hover fieldset': { borderColor: '#80deea', },
                                    '&.Mui-focused fieldset': { borderColor: '#2e86c1 ', },
                                },
                            }}
                        />
                    </FormControl>
                    <Button
                        type="submit"
                        variant="contained"
                        color="primary"
                        disabled={isLoading}
                        sx={{
                            height: '48px',
                            marginTop: '12px',
                            '&:hover': { transform: 'scale(1.02)', },
                            '&:active': { transform: 'scale(0.98)', },
                        }}
                    >
                        {isLoading ? <CircularProgress size={24} sx={{ color: 'white' }} /> : 'Log in'}
                    </Button>
                </form>
                <Link
                    href="/forgot-password"
                    sx={{
                        display: 'inline-flex',
                        alignItems: 'center',
                        color: '#2196F3',
                        fontWeight: '600',
                        textDecoration: 'none',
                        '&:hover': {
                            color: '#1e88e5',
                            textDecoration: 'underline',
                            transform: 'translateX(3px)',
                            transition: 'transform 0.2s ease, color 0.3s ease',
                        },
                        fontSize: '14px',
                        marginTop: '1px',
                        fontFamily: 'Arial, sans-serif',
                    }}
                >
                    Forgot Password?
                </Link>

                {error && (
                    <Typography sx={{ color: '#FF0000', fontWeight: 'bold', fontSize: '18px', marginBottom: '15px', display: 'flex', alignItems: 'center', }}>
                        <ErrorIcon sx={{ marginRight: '8px' }} />
                        {error}
                    </Typography>
                )}
            </Box>
            <Snackbar open={openSnackbar} autoHideDuration={4000} onClose={handleCloseSnackbar} anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}>
                <Alert onClose={handleCloseSnackbar}
                    // @ts-ignore
                    severity={snackbarSeverity}>
                    {snackbarMessage}
                </Alert>
            </Snackbar>
        </main>
    );
};

export default Login;
