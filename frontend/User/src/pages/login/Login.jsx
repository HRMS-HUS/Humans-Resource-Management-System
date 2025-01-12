import Sheet from '@mui/joy/Sheet';
import Typography from '@mui/joy/Typography';
import FormControl from '@mui/joy/FormControl';
import FormLabel from '@mui/joy/FormLabel';
import Input from '@mui/joy/Input';
import ErrorIcon from '@mui/icons-material/Error';
import LoadingButton from '@mui/lab/LoadingButton';
import Link from '@mui/joy/Link';
import { Box } from '@mui/material';
import { useState } from 'react';
import { useAuthStore } from './authStore';

const Login = () => {

    const [username, setUsername] = useState('')
    const [password, setPassword] = useState('')
    const { login, error, isLoading } = useAuthStore()

    const handleLogin = async (e) => {
        e.preventDefault()
        await login(username, password)
    }

    return (
        <main style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh', margin: 0, backgroundImage: 'url("https://images4.alphacoders.com/211/thumb-1920-211006.jpg")', backgroundSize: 'cover', backgroundPosition: 'center', }}>
            <Sheet sx={{ width: 370, mx: 'auto', my: 4, py: 3, px: 2, display: 'flex', flexDirection: 'column', gap: 2, borderRadius: 'sm', boxShadow: 'md', background: 'transparent', backgroundColor: 'rgba(128, 128, 128, 0.6)' }} variant="outlined">
                <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', height: '28vh', textAlign: 'center', }}>
                    <img src={'https://cdnlogo.com/logos/n/71/nvidia.svg'} style={{ width: 120, height: 120 }} />
                    <Typography level="h2" component="h1"><b>Welcome to NVIDIA!</b></Typography>
                </Box>
                <form onSubmit={handleLogin} style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
                    <FormControl>
                        <FormLabel sx={{ fontSize: '16px' }}>Username</FormLabel>
                        <Input name="username" type="text" placeholder="Username" sx={{ height: '42px', backgroundColor: 'rgba(128, 128, 128, 0.6)' }} onChange={(e) => setUsername(e.target.value)} />
                    </FormControl>
                    <FormControl>
                        <FormLabel sx={{ fontSize: '16px' }}>Password</FormLabel>
                        <Input name="password" type="password" placeholder="Password" sx={{ height: '42px', backgroundColor: 'rgba(128, 128, 128, 0.6)' }} onChange={(e) => setPassword(e.target.value)} />
                    </FormControl>
                    <LoadingButton
                        type='submit'
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
                        Log in
                    </LoadingButton>
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
                        fontSize: '16px',
                        marginTop: '10px',
                    }}
                >
                    Forgot Password?
                </Link>
                {error &&
                    <Typography sx={{ color: '#FF0000', fontWeight: 'bold', fontSize: '18px', marginTop: '1px', display: 'flex', alignItems: 'center', }}>
                        <span style={{ marginRight: '8px', display: 'flex', alignItems: 'center' }}>
                            <ErrorIcon />
                        </span>
                        {error}
                    </Typography>
                }
            </Sheet>
        </main>
    )
}

export default Login