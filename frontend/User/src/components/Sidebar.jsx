import React, { useEffect, useState } from 'react';
import { NavLink, useNavigate } from 'react-router-dom';
import { Grid, CheckSquare, Calendar, DollarSign, LogOut } from 'lucide-react';
import axios from 'axios';
import { useAuthStore } from '../pages/login/authStore';
import '../styles/Sidebar.css';

const Sidebar = () => {
  const navigate = useNavigate();
  const { logout } = useAuthStore();
  const [userProfile, setUserProfile] = useState({
    name: '',
    department: '',
    avatar_url: '',
  });

  useEffect(() => {
    const fetchUserData = async () => {
      try {
        const personalInfoResponse = await axios.get('http://52.184.86.56:8000/api/personal_info', {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`
          }
        });

        const departmentResponse = await axios.get('http://52.184.86.56:8000/api/department', {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`
          }
        });

        setUserProfile({
          name: personalInfoResponse.data.fullname || 'Tên người dùng',
          department: departmentResponse.data.name || 'Phòng ban',
          avatar_url: personalInfoResponse.data.photo_url || '/api/placeholder/64/64'
        });
      } catch (error) {
        console.error('Lỗi khi lấy thông tin cá nhân:', error);
        setUserProfile({
          name: 'Tên người dùng',
          department: 'Phòng ban',
          avatar_url: '/api/placeholder/64/64'
        });
      }
    };

    fetchUserData();
  }, []);

  const handleLogout = () => {
    logout(); // Call logout function from authStore
    navigate('/login'); // Navigate to login page
  };

  return (
    <div className="sidebar">
      <div className="profile">
        <div className="avatar">
          <img src={userProfile.avatar_url} alt="Avatar" />
        </div>
        <div className="name-user">{userProfile.name}</div>
        <div className="name-department">{userProfile.department}</div>
      </div>
      <div className="menu">
        <NavLink to="/" className={({ isActive }) => `menu-item ${isActive ? 'active' : ''}`}>
          <div id="icon"><Grid size={20} /></div>
          <div>Tổng quan</div>
        </NavLink>
        <NavLink to="/attendance" className={({ isActive }) => `menu-item ${isActive ? 'active' : ''}`}>
          <div id="icon"><CheckSquare size={20} /></div>
          <div>Chấm công</div>
        </NavLink>
        <NavLink to="/schedule" className={({ isActive }) => `menu-item ${isActive ? 'active' : ''}`}>
          <div id="icon"><Calendar size={20} /></div>
          <div>Lịch trình</div>
        </NavLink>
        <NavLink to="/salary" className={({ isActive }) => `menu-item ${isActive ? 'active' : ''}`}>
          <div id="icon"><DollarSign size={20} /></div>
          <div>Lương</div>
        </NavLink>
      </div>
      <div 
        className="logout"
        onClick={handleLogout}
        style={{ 
          cursor: 'pointer',
          display: 'flex',
          alignItems: 'center',
          gap: '8px',
          justifyContent: 'center'
        }}
      >
        <LogOut size={20} />
        <span>Đăng xuất</span>
      </div>
    </div>
  );
};

export default Sidebar;