import React, { useEffect, useRef, useState } from 'react';
import PropTypes from 'prop-types';
import { Input as BaseInput } from '@mui/base/Input';
import { Box, Typography, FormControl, InputLabel, OutlinedInput, Button, Snackbar, Alert, TextField, FormLabel } from '@mui/material';
import { styled } from '@mui/system';
import { useNavigate } from 'react-router-dom';
import { useAuthStore } from './authStore';

const InputElement = styled('input')`
  width: 42px;
  font-family: 'Roboto', sans-serif;
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
  const inputRefs = React.useRef(new Array(length).fill(null));

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
          const otp =
            prevOtp.slice(0, currentIndex) + prevOtp.slice(currentIndex + 1);
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
          const otp =
            prevOtp.slice(0, currentIndex) + prevOtp.slice(currentIndex + 1);
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

    // Check if there is text data in the clipboard
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
  const navigate = useNavigate();
  const [otp, setOtp] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [openSnackbar, setOpenSnackbar] = useState(false);
  const [snackbarMessage, setSnackbarMessage] = useState('');
  const { resetPassword, email } = useAuthStore()

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (newPassword !== confirmPassword) {
      setSnackbarMessage('Passwords do not match');
      setOpenSnackbar(true);
      return;
    }

    await resetPassword(email, otp, newPassword, confirmPassword)

    setSnackbarMessage('Password reset successfully! Redirecting to login...');
    setOpenSnackbar(true);
    setTimeout(() => {
      navigate('/login');
    }, 3000);
  };

  const handleCloseSnackbar = () => {
    setOpenSnackbar(false);
  };

  return (
    <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh', backgroundImage: 'url("https://vti-solutions.vn/wp-content/uploads/2022/09/xu-huong-quan-tri-nhan-su.png")', backgroundSize: 'cover', backgroundPosition: 'center', }}>
      <Box sx={{ width: 430, p: 3, display: 'flex', flexDirection: 'column', gap: 2, borderRadius: 2, backgroundColor: 'rgba(128, 128, 128, 0.9)', border: '0.5px solid #b2ebf2' }}>
        <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', height: '28vh', textAlign: 'center', mt: 3, gap: 0.5 }}>
          <img src={'https://cdn.haitrieu.com/wp-content/uploads/2021/12/hai-trieu-favicon.png'} style={{ width: 120, height: 120 }} />
          <Typography variant="h4" gutterBottom sx={{ fontSize: '30px', color: 'rgba(0, 0, 0, 0.7)' }}><b>Reset Password</b></Typography>
          <Typography sx={{ color: 'rgba(0, 0, 0, 0.7)' }}>Enter the OTP and the new password you want to reset.</Typography>
        </Box>
        <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '25px' }}>
          <FormControl sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
            <OTP separator={<span></span>} value={otp} onChange={setOtp} length={6} />
          </FormControl>
          <TextField
            placeholder="New Password"
            variant="outlined"
            type="password"
            value={newPassword}
            onChange={(e) => setNewPassword(e.target.value)}
            fullWidth
            InputProps={{ sx: { backgroundColor: '#f5f5f5', height: '43px', }, }}
          />
          <TextField
            placeholder="Confirm Password"
            variant="outlined"
            type="password"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
            fullWidth
            InputProps={{ sx: { backgroundColor: '#f5f5f5', height: '43px', }, }}
          />
          <Button type="submit" variant="contained" color="primary" fullWidth sx={{ marginTop: '12px', height: '48px', fontWeight: 'bold' }}>Reset Password</Button>
        </form>
      </Box>
      <Snackbar
        open={openSnackbar}
        autoHideDuration={4000}
        onClose={handleCloseSnackbar}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
      >
        <Alert
          onClose={handleCloseSnackbar}
          severity={snackbarMessage.includes('successfully') ? 'success' : 'error'}
        >
          {snackbarMessage}
        </Alert>
      </Snackbar>
    </Box>
  );
};

export default ResetPassword;
