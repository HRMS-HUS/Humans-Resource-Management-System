import Sheet from '@mui/joy/Sheet';
import Typography from '@mui/joy/Typography';
import FormControl from '@mui/joy/FormControl';
import FormLabel from '@mui/joy/FormLabel';
import Input from '@mui/joy/Input';
import Button from '@mui/joy/Button';
import Link from '@mui/joy/Link';
import { Box } from '@mui/material';
import { useState } from 'react';
import { useAuthStore } from './authStore';

const Login = () => {

    const [username, setUsername] = useState('')
    const [password, setPassword] = useState('')
    const { login } = useAuthStore()

    const handleLogin = async (e) => {
        e.preventDefault()
        await login(username, password)
    }

    return (
        <main style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh', margin: 0, backgroundImage: 'url("https://images4.alphacoders.com/211/thumb-1920-211006.jpg")', backgroundSize: 'cover', backgroundPosition: 'center', }}>
            <Sheet sx={{ width: 370, mx: 'auto', my: 4, py: 3, px: 2, display: 'flex', flexDirection: 'column', gap: 2, borderRadius: 'sm', boxShadow: 'md', background: 'transparent' }} variant="outlined">
                <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', height: '28vh', textAlign: 'center', }}>
                    <img src={'https://cdnlogo.com/logos/n/71/nvidia.svg'} style={{ width: 120, height: 120 }} />
                    <Typography level="h2" component="h1"><b>Welcome to NVIDIA!</b></Typography>
                </Box>
                <form onSubmit={handleLogin} style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
                    <FormControl>
                        <FormLabel sx={{ fontSize: '16px' }}>Username</FormLabel>
                        <Input name="username" type="text" placeholder="Username" sx={{ height: '40px' }} onChange={(e) => setUsername(e.target.value)} />
                    </FormControl>
                    <FormControl>
                        <FormLabel sx={{ fontSize: '16px' }}>Password</FormLabel>
                        <Input name="password" type="password" placeholder="Password" sx={{ height: '40px' }} onChange={(e) => setPassword(e.target.value)} />
                    </FormControl>
                    <Button sx={{ mt: 1, fontSize: '16px' }}>Log in</Button>
                </form>
                <Link href="/forgot-password" sx={{ color: "#1976d2" }}>Forgot password?</Link>
            </Sheet>
        </main>
    )
}

export default Login
