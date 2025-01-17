import React, { useState } from 'react';
import { Eye, EyeOff, KeyRound } from 'lucide-react';
import axios from 'axios';
import "../styles/ChangePass.css";

const ChangePassword = () => {
  const [formData, setFormData] = useState({
    currentPassword: '',
    newPassword: '',
    confirmPassword: ''
  });

  const [errors, setErrors] = useState({});
  const [showCurrentPassword, setShowCurrentPassword] = useState(false);
  const [showNewPassword, setShowNewPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [message, setMessage] = useState({ type: '', text: '' });

  const validateForm = () => {
    const newErrors = {};

    if (!formData.currentPassword) {
      newErrors.currentPassword = 'Vui lòng nhập mật khẩu hiện tại';
    }

    if (!formData.newPassword) {
      newErrors.newPassword = 'Vui lòng nhập mật khẩu mới';
    } else if (formData.newPassword.length < 6) {
      newErrors.newPassword = 'Mật khẩu mới phải có ít nhất 6 ký tự';
    }

    if (!formData.confirmPassword) {
      newErrors.confirmPassword = 'Vui lòng xác nhận mật khẩu mới';
    } else if (formData.newPassword !== formData.confirmPassword) {
      newErrors.confirmPassword = 'Mật khẩu xác nhận không khớp';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMessage({ type: '', text: '' });

    if (!validateForm()) return;

    setIsLoading(true);

    try {
      const token = localStorage.getItem('token');
      const response = await axios.put(
        'http://52.184.86.56:8000/api/me/user/change-password',
        null,  // No body in the request, we will pass the params
        {
          params: {
            current_password: formData.currentPassword,
            new_password: formData.newPassword
          },
          headers: {
            Authorization: `Bearer ${token}`
          }
        }
      );

      setMessage({ type: 'success', text: 'Password change successful!' });
      setFormData({ currentPassword: '', newPassword: '', confirmPassword: '' });
    } catch (error) {
      console.error('Error changing password:', error);
      setMessage({
        type: 'error',
        text: error.response?.data?.message || 'An error occurred when changing the password'
      });
    } finally {
      setIsLoading(false);
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value
    }));
    // Clear error when user starts typing
    if (errors[name]) {
      setErrors((prev) => ({
        ...prev,
        [name]: ''
      }));
    }
  };

  return (
    <div className="rectangle-container">
      <div className="form-wrapper">
        {/* Header */}
        <div className="header-password">
          <div className="flex items-center gap-2 text-xl font-semibold">
            <KeyRound className="icon" />
            Change password
          </div>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit} className="form-fields">
          {/* Current Password */}
          <div className="input-container">
            <label className="label-text">
            Current Password
            </label>
            <div className="input-field-wrapper">
              <input
                type={showCurrentPassword ? 'text' : 'password'}
                name="currentPassword"
                value={formData.currentPassword}
                onChange={handleChange}
                className={`input-field ${errors.currentPassword ? 'error' : ''}`}
              />
              <button
                type="button"
                onClick={() => setShowCurrentPassword(!showCurrentPassword)}
                className="eye-button"
              >
                {showCurrentPassword ? (
                  <EyeOff className="icon" />
                ) : (
                  <Eye className="icon" />
                )}
              </button>
            </div>
            {errors.currentPassword && (
              <p className="error-text">{errors.currentPassword}</p>
            )}
          </div>

          {/* New Password */}
          <div className="input-container">
            <label className="label-text">
            New Password
            </label>
            <div className="input-field-wrapper">
              <input
                type={showNewPassword ? 'text' : 'password'}
                name="newPassword"
                value={formData.newPassword}
                onChange={handleChange}
                className={`input-field ${errors.newPassword ? 'error' : ''}`}
              />
              <button
                type="button"
                onClick={() => setShowNewPassword(!showNewPassword)}
                className="eye-button"
              >
                {showNewPassword ? (
                  <EyeOff className="icon" />
                ) : (
                  <Eye className="icon" />
                )}
              </button>
            </div>
            {errors.newPassword && (
              <p className="error-text">{errors.newPassword}</p>
            )}
          </div>

          {/* Confirm Password */}
          <div className="input-container">
            <label className="label-text">
            Confirm the new password
            </label>
            <div className="input-field-wrapper">
              <input
                type={showConfirmPassword ? 'text' : 'password'}
                name="confirmPassword"
                value={formData.confirmPassword}
                onChange={handleChange}
                className={`input-field ${errors.confirmPassword ? 'error' : ''}`}
              />
              <button
                type="button"
                onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                className="eye-button"
              >
                {showConfirmPassword ? (
                  <EyeOff className="icon" />
                ) : (
                  <Eye className="icon" />
                )}
              </button>
            </div>
            {errors.confirmPassword && (
              <p className="error-text">{errors.confirmPassword}</p>
            )}
          </div>

          {/* Message Display */}
          {message.text && (
            <div
              className={`message-box ${message.type === 'success' ? 'success' : 'error'}`}
            >
              {message.text}
            </div>
          )}

          {/* Submit Button */}
          <button
            type="submit"
            disabled={isLoading}
            className={`submit-button ${isLoading ? 'loading' : ''}`}
          >
            {isLoading ? 'Processing...' : 'Change password'}
          </button>
        </form>
      </div>
    </div>
  );
};

export default ChangePassword;
