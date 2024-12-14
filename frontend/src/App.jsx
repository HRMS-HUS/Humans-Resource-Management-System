import React, { useState } from "react";
import "./App.css";
const Login = () => {
  const [passwordType, setPasswordType] = useState("password");

  const togglePasswordVisibility = () => {
    setPasswordType(passwordType === "password" ? "text" : "password");
  };

  return (
    <div id="wrapper">
      <form>
        <h3>Đăng nhập</h3>
        <div className="form-group">
          <input type="text" name="username" required />
          <label>Tài khoản</label>
        </div>
        <div className="form-group password-wrapper">
          <input type={passwordType} name="password" id="password" required />
          <label>Mật khẩu</label>
          <span className="toggle-password" onClick={togglePasswordVisibility}>
            {passwordType === "password" ? "\u{1F441}" : "\u{1F441}\u{FE0E}"}
          </span>
        </div>
        <input type="submit" value="Đăng nhập" id="btn-login" />
        <div className="forgot-password">
          <a href="#">Quên mật khẩu</a>
        </div>
      </form>
    </div>
  );
};

export default Login;
