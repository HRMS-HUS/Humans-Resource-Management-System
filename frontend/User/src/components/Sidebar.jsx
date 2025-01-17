import React, { useEffect, useState } from 'react';
import { NavLink, useNavigate } from 'react-router-dom';
import { Grid, CheckSquare, Calendar, DollarSign, LogOut, CalendarX, Shell, CircleUser } from 'lucide-react';
import axios from 'axios';
import imageCompression from 'browser-image-compression';
import { useAuthStore } from '../pages/login/authStore';
import '../styles/Sidebar.css';

const Sidebar = () => {
  const navigate = useNavigate();
  const { logout } = useAuthStore();
  const userName = useAuthStore(state => state.userName);
  const [userProfile, setUserProfile] = useState({
    id: '',
    department: '',
    avatar_url: '',
  });
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedFile, setSelectedFile] = useState(null);

  useEffect(() => {
    const fetchUserData = async () => {
      try {
        const token = localStorage.getItem('token');
        if (!token) {
          console.error('The token does not exist. The user needs to log in again.');
          logout();
          return navigate('/login');
        }

        const config = {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        };

        const [personalInfoResponse, departmentResponse] = await Promise.all([
          axios.get('http://52.184.86.56:8000/api/me/personal_info', config),
          axios.get('http://52.184.86.56:8000/api/me/department', config),
        ]);

        setUserProfile({
          id: personalInfoResponse.data.user_id || 'No ID',
          department: departmentResponse.data.name || 'No department',
          avatar_url:
            personalInfoResponse.data.photo_url ||
            'https://th.bing.com/th/id/OIP.4XXJ7fxuB4gkO5DVNHxMGwAAAA?w=154&h=160&c=7&r=0&o=5&dpr=1.4&pid=1.7',
        });
      } catch (error) {
        console.error('Error retrieving user information:', error.message);
        if (error.response?.status === 401) {
          logout();
          localStorage.removeItem('token');
          return navigate('/login');
        }
      }
    };

    fetchUserData();
  }, [logout, navigate]);

  const handleLogout = async () => {
    try {
      const token = localStorage.getItem('token');
      if (!token) {
        console.error('No tokens found. Cancel the logout.');
        return;
      }
  
      const logoutTime = new Date().toISOString();
      await axios.post(
        'http://52.184.86.56:8000/api/logout/me',
        { logout_time: logoutTime },
        { headers: { Authorization: `Bearer ${token}` } }
      );
  
      localStorage.removeItem('token');
      logout();
      navigate('/login');
    } catch (error) {
      console.error('Error sending logout data:', error);
    }
  };

  const handleFileChange = (e) => {
    setSelectedFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      alert('Please select the file before uploading.');
      return;
    }
  
    try {
      const compressedFile = await imageCompression(selectedFile, {
        maxSizeMB: 0.5,
        maxWidthOrHeight: 1024,
        useWebWorker: true,
      });
  
      const formData = new FormData();
      formData.append('file', compressedFile);
  
      const token = localStorage.getItem('token');
      if (!token) {
        throw new Error('No tokens found. Unload the photo.');
      }
  
      const personalInfoResponse = await axios.get(
        'http://52.184.86.56:8000/api/me/personal_info',
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );
  
      const personalInfoId = personalInfoResponse.data.user_id;
      
      if (!personalInfoId) {
        throw new Error('Không tìm thấy personal_info_id');
      }
  
      const config = {
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'multipart/form-data',
        },
      };
  
      const response = await axios.put(
        `http://52.184.86.56:8000/api/me/personal_info/${personalInfoId}/photo`,
        formData,
        config
      );
  
      setUserProfile((prev) => ({
        ...prev,
        avatar_url: response.data.photo_url,
      }));
  
      alert('The photo has been uploaded successfully!');
      setIsModalOpen(false);
    } catch (error) {
      console.error('Error uploading photos:', error);
      
      let errorMessage = 'An error occurred when uploading photos.';
      
      if (error.response) {
        if (error.response.status === 404) {
          errorMessage = 'No user information found.';
        } else if (error.response.status === 401) {
          errorMessage = 'The login session has expired. Please log in again.';
          logout();
          navigate('/login');
        }
      }
      
      alert(errorMessage);
    }
  };

  return (
    <div className="sidebar">
      <div className="profile">
        <div className="avatar" onClick={() => setIsModalOpen(true)} style={{ cursor: 'pointer' }}>
          <img src={userProfile.avatar_url} alt="Avatar" />
        </div>
        <div className="name-user">{userName || 'No name'}</div>
        <div className="name-department">{userProfile.department}</div>
      </div>

      <div className="menu">
        <NavLink to="/" className={({ isActive }) => `menu-item ${isActive ? 'active' : ''}`}>
          <div id="icon">
            <Grid size={20} />
          </div>
          <div>Overview</div>
        </NavLink>
        <NavLink to="/attendance" className={({ isActive }) => `menu-item ${isActive ? 'active' : ''}`}>
          <div id="icon">
            <CheckSquare size={20} />
          </div>
          <div>Login history</div>
        </NavLink>
        <NavLink to="/schedule" className={({ isActive }) => `menu-item ${isActive ? 'active' : ''}`}>
          <div id="icon">
            <Calendar size={20} />
          </div>
          <div>Itinerary</div>
        </NavLink>
        <NavLink to="/salary" className={({ isActive }) => `menu-item ${isActive ? 'active' : ''}`}>
          <div id="icon">
            <DollarSign size={20} />
          </div>
          <div>Salary</div>
        </NavLink>
        <NavLink to="/holiday" className={({ isActive }) => `menu-item ${isActive ? 'active' : ''}`}>
          <div id="icon">
            <CalendarX size={20} />
          </div>
          <div>Holidays</div>
        </NavLink>
        <NavLink to="/application" className={({ isActive }) => `menu-item ${isActive ? 'active' : ''}`}>
          <div id="icon">
            <Shell size={20} />
          </div>
          <div>Application</div>
        </NavLink>
        <NavLink to="/user-info" className={({ isActive }) => `menu-item ${isActive ? 'active' : ''}`}>
          <div id="icon">
            <CircleUser size={20} />
          </div>
          <div>Personal Information</div>
        </NavLink>
        <NavLink to="/change-password" className={({ isActive }) => `menu-item ${isActive ? 'active' : ''}`}>
          <div id="icon">
            <CircleUser size={20} />
          </div>
          <div>Change Password</div>
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
          justifyContent: 'center',
        }}
      >
        <LogOut size={20} />
        <span>Log out</span>
      </div>

      {isModalOpen && (
        <div className="modal-overlay">
          <div className="modal-content">
            <img className="modal-avatar" src={userProfile.avatar_url} alt="Phóng to Avatar" />
            <input className="input-file" type="file" onChange={handleFileChange} />
            <button onClick={handleUpload}>Upload avatar</button>
            <button onClick={() => setIsModalOpen(false)}>Cancle</button>
          </div>
        </div>
      )}
    </div>
  );
};

export default Sidebar;