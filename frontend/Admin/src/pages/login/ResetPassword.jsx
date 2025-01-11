import * as React from 'react';
import { Input as BaseInput } from '@mui/base/Input';
import PropTypes from 'prop-types';
import Sheet from '@mui/joy/Sheet';
import Typography from '@mui/joy/Typography';
import FormControl from '@mui/joy/FormControl';
import FormLabel from '@mui/joy/FormLabel';
import Input from '@mui/joy/Input';
import LoadingButton from '@mui/lab/LoadingButton';
import { Box, Snackbar, Alert } from '@mui/material';
import { useEffect, useRef, useState } from 'react';
import { useAuthStore } from './authStore';
import { useNavigate } from 'react-router-dom';
import { styled } from '@mui/system';
import './Image.css'

const InputElement = styled('input')`
  width: 42px;
  font-family: 'IBM Plex Sans', sans-serif;
  font-size: 1rem;
  font-weight: 550;
  line-height: 1.5;
  padding: 8px 0;
  border-radius: 8px;
  text-align: center;
  color: #F5F5F5;
  background: rgba(128, 128, 128, 0.9);
  border: 1px solid #e0e0e0;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  &:hover { border-color: #1e90ff; }
  &:focus { border-color: #1e90ff; box-shadow: 0 0 0 3px rgba(30, 144, 255, 0.5); }
  &:focus-visible { outline: 0; }
`;

function OTP({ separator, length, value, onChange }) {
    const inputRefs = useRef(new Array(length).fill(null));

    const focusInput = (targetIndex) => {
        const targetInput = inputRefs.current[targetIndex];
        targetInput.focus();
    };

    const selectInput = (targetIndex) => {
        const targetInput = inputRefs.current[targetIndex];
        targetInput.select();
    };

    const handleKeyDown = (event, currentIndex) => {
        switch (event.key) {
            case 'ArrowUp':
            case 'ArrowDown':
            case ' ':
                event.preventDefault();
                break;
            case 'ArrowLeft':
                event.preventDefault();
                if (currentIndex > 0) {
                    focusInput(currentIndex - 1);
                    selectInput(currentIndex - 1);
                }
                break;
            case 'ArrowRight':
                event.preventDefault();
                if (currentIndex < length - 1) {
                    focusInput(currentIndex + 1);
                    selectInput(currentIndex + 1);
                }
                break;
            case 'Delete':
                event.preventDefault();
                onChange((prevOtp) => {
                    const otp = prevOtp.slice(0, currentIndex) + prevOtp.slice(currentIndex + 1);
                    return otp;
                });

                break;
            case 'Backspace':
                event.preventDefault();
                if (currentIndex > 0) {
                    focusInput(currentIndex - 1);
                    selectInput(currentIndex - 1);
                }

                onChange((prevOtp) => {
                    const otp = prevOtp.slice(0, currentIndex) + prevOtp.slice(currentIndex + 1);
                    return otp;
                });
                break;

            default:
                break;
        }
    };

    const handleChange = (event, currentIndex) => {
        const currentValue = event.target.value;
        let indexToEnter = 0;

        while (indexToEnter <= currentIndex) {
            if (inputRefs.current[indexToEnter].value && indexToEnter < currentIndex) {
                indexToEnter += 1;
            } else {
                break;
            }
        }
        onChange((prev) => {
            const otpArray = prev.split('');
            const lastValue = currentValue[currentValue.length - 1];
            otpArray[indexToEnter] = lastValue;
            return otpArray.join('');
        });
        if (currentValue !== '') {
            if (currentIndex < length - 1) {
                focusInput(currentIndex + 1);
            }
        }
    };

    const handleClick = (event, currentIndex) => {
        selectInput(currentIndex);
    };

    const handlePaste = (event, currentIndex) => {
        event.preventDefault();
        const clipboardData = event.clipboardData;

        if (clipboardData.types.includes('text/plain')) {
            let pastedText = clipboardData.getData('text/plain');
            pastedText = pastedText.substring(0, length).trim();
            let indexToEnter = 0;

            while (indexToEnter <= currentIndex) {
                if (inputRefs.current[indexToEnter].value && indexToEnter < currentIndex) {
                    indexToEnter += 1;
                } else {
                    break;
                }
            }

            const otpArray = value.split('');

            for (let i = indexToEnter; i < length; i += 1) {
                const lastValue = pastedText[i - indexToEnter] ?? ' ';
                otpArray[i] = lastValue;
            }

            onChange(otpArray.join(''));
        }
    };

    return (
        <Box sx={{ display: 'flex', gap: 1, alignItems: 'center' }}>
            {new Array(length).fill(null).map((_, index) => (
                <React.Fragment key={index}>
                    <BaseInput
                        slots={{
                            input: InputElement,
                        }}
                        aria-label={`Digit ${index + 1} of OTP`}
                        slotProps={{
                            input: {
                                ref: (ele) => {
                                    inputRefs.current[index] = ele;
                                },
                                onKeyDown: (event) => handleKeyDown(event, index),
                                onChange: (event) => handleChange(event, index),
                                onClick: (event) => handleClick(event, index),
                                onPaste: (event) => handlePaste(event, index),
                                value: value[index] ?? '',
                            },
                        }}
                    />
                    {index === length - 1 ? null : separator}
                </React.Fragment>
            ))}
        </Box>
    );
}

OTP.propTypes = {
    length: PropTypes.number.isRequired,
    onChange: PropTypes.func.isRequired,
    separator: PropTypes.node,
    value: PropTypes.string.isRequired,
};

const ResetPassword = () => {

    const navigate = useNavigate()
    const [username, setUsername] = useState("")
    const [otp, setOtp] = useState("")
    const [newPassword, setNewPassword] = useState("")
    const [confirmPassword, setConfirmPassword] = useState("")
    const [openSnackbar, setOpenSnackbar] = useState(false);
    const [snackbarMessage, setSnackbarMessage] = useState("");
    const { isLoading, resetPassword } = useAuthStore()

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
            <Sheet sx={{ width: 430, mx: 'auto', my: 4, py: 3, px: 2, display: 'flex', flexDirection: 'column', gap: 2, borderRadius: 'sm', boxShadow: 'md', background: 'transparent', backgroundColor: 'rgba(128, 128, 128, 0.3)' }} variant="outlined">
                <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', height: '28vh', textAlign: 'center', }}>
                    <img src={'https://cdnlogo.com/logos/n/71/nvidia.svg'} className="rotate-img" alt="NVIDIA logo" />
                    <Typography level="h2" component="h1"><b>Reset Password</b></Typography>
                    <Typography>Please enter the OTP code and the new password you want to reset.</Typography>
                </Box>
                <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
                    <FormControl>
                        <FormLabel sx={{ fontSize: '16px' }}>Username</FormLabel>
                        <Input name="username" type="text" placeholder="Username" sx={{ height: '45px', backgroundColor: 'rgba(128, 128, 128, 0.8)', }} onChange={(e) => setUsername(e.target.value)} />
                    </FormControl>
                    <FormControl>
                        <FormLabel sx={{ fontSize: '16px' }}>OTP</FormLabel>
                        <OTP separator={<span></span>} value={otp} onChange={setOtp} length={6} />
                    </FormControl>
                    <Box style={{ display: 'flex', gap: '16px' }}>
                        <FormControl style={{ flex: 1 }}>
                            <FormLabel sx={{ fontSize: '16px' }}>New Password</FormLabel>
                            <Input name="new_password" type="password" placeholder="New Password" sx={{ height: '45px', backgroundColor: 'rgba(128, 128, 128, 0.8)' }} onChange={(e) => setNewPassword(e.target.value)} />
                        </FormControl>
                        <FormControl style={{ flex: 1 }}>
                            <FormLabel sx={{ fontSize: '16px' }}>Confirm Password</FormLabel>
                            <Input name="confirm_password" type="password" placeholder="Confirm Password" sx={{ height: '45px', backgroundColor: 'rgba(128, 128, 128, 0.8)' }} onChange={(e) => setConfirmPassword(e.target.value)} />
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
