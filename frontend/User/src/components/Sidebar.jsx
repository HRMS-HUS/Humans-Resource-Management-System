import React, { useEffect, useState } from 'react';
import { NavLink, useNavigate } from 'react-router-dom';
import { Grid, CheckSquare, Calendar, DollarSign, LogOut, CalendarX, Shell,CircleUser  } from 'lucide-react';
import axios from 'axios';
import imageCompression from 'browser-image-compression';
import { useAuthStore } from '../pages/login/authStore';
import '../styles/Sidebar.css';

const Sidebar = () => {
  const navigate = useNavigate();
  const { logout } = useAuthStore();
  const [userProfile, setUserProfile] = useState({
    name: '',
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
          console.error('Token không tồn tại. Người dùng cần đăng nhập lại.');
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
          name: personalInfoResponse.data.fullname || 'Không có tên',
          id: personalInfoResponse.data.user_id || 'Không có ID',
          department: departmentResponse.data.name || 'Không rõ phòng ban',
          avatar_url:
            personalInfoResponse.data.photo_url ||
            'https://th.bing.com/th/id/OIP.4XXJ7fxuB4gkO5DVNHxMGwAAAA?w=154&h=160&c=7&r=0&o=5&dpr=1.4&pid=1.7',
        });
      } catch (error) {
        console.error('Lỗi khi lấy thông tin người dùng:', error.message);
        if (error.response?.status === 401) {
          logout();
          localStorage.removeItem('token');
          return navigate('/login');
        }
      }
    };

    fetchUserData();
  }, [logout, navigate]);

  const handleLogout = () => {
    localStorage.removeItem('token'); // Xóa token khỏi localStorage
    logout(); // Đăng xuất người dùng
    navigate('/login'); // Chuyển hướng đến trang đăng nhập
  };

  const handleFileChange = (e) => {
    setSelectedFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      alert('Vui lòng chọn tệp trước khi tải lên.');
      return;
    }
  
    try {
      // Nén ảnh trước khi tải lên
      const compressedFile = await imageCompression(selectedFile, {
        maxSizeMB: 0.5,
        maxWidthOrHeight: 1024,
        useWebWorker: true,
      });
  
      // Tạo FormData
      const formData = new FormData();
      formData.append('photo', compressedFile);
  
      const token = localStorage.getItem('token');
      if (!token) {
        console.error('Không tìm thấy token. Hủy tải ảnh.');
        return;
      }
  
      // Cấu hình headers
      const config = {
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'multipart/form-data',
        },
      };
  
      // Gửi yêu cầu API
      const response = await axios.put(
        `http://52.184.86.56:8000/api/me/${userProfile.id}/photo`,
        formData,
        config
      );
  
      // Cập nhật avatar URL mới
      setUserProfile((prev) => ({
        ...prev,
        avatar_url: response.data.photo_url,
      }));
  
      alert('Ảnh đã được tải lên thành công!');
      setIsModalOpen(false);
    } catch (error) {
      console.error('Lỗi khi tải lên ảnh:', error);
      if (error.response) {
        console.error('Phản hồi từ server:', error.response.data);
      }
      alert('Có lỗi xảy ra khi tải lên ảnh.');
    }
  };
  

  return (
    <div className="sidebar">
      <div className="profile">
        <div className="avatar" onClick={() => setIsModalOpen(true)} style={{ cursor: 'pointer' }}>
          <img src={userProfile.avatar_url} alt="Avatar" />
        </div>
        <div className="name-user">{userProfile.name}</div>
        <div className="name-department">{userProfile.department}</div>
      </div>

      <div className="menu">
        <NavLink to="/" className={({ isActive }) => `menu-item ${isActive ? 'active' : ''}`}>
          <div id="icon">
            <Grid size={20} />
          </div>
          <div>Tổng quan</div>
        </NavLink>
        <NavLink to="/attendance" className={({ isActive }) => `menu-item ${isActive ? 'active' : ''}`}>
          <div id="icon">
            <CheckSquare size={20} />
          </div>
          <div>Lịch sử đăng nhập</div>
        </NavLink>
        <NavLink to="/schedule" className={({ isActive }) => `menu-item ${isActive ? 'active' : ''}`}>
          <div id="icon">
            <Calendar size={20} />
          </div>
          <div>Lịch trình</div>
        </NavLink>
        <NavLink to="/salary" className={({ isActive }) => `menu-item ${isActive ? 'active' : ''}`}>
          <div id="icon">
            <DollarSign size={20} />
          </div>
          <div>Lương</div>
        </NavLink>
        <NavLink to="/holiday" className={({ isActive }) => `menu-item ${isActive ? 'active' : ''}`}>
          <div id="icon">
            <CalendarX size={20} />
          </div>
          <div>Ngày lễ</div>
        </NavLink>
        <NavLink to="/application" className={({ isActive }) => `menu-item ${isActive ? 'active' : ''}`}>
          <div id="icon">
            <Shell size={20} />
          </div>
          <div>Xin nghỉ</div>
        </NavLink>
        <NavLink to="/user-info" className={({ isActive }) => `menu-item ${isActive ? 'active' : ''}`}>
          <div id="icon">
            <CircleUser size={20} />
          </div>
          <div>Thông tin cá nhân</div>
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
        <span>Đăng xuất</span>
      </div>

      {isModalOpen && (
        <div className="modal-overlay">
          <div className="modal-content">
            <img className="modal-avatar" src={userProfile.avatar_url} alt="Phóng to Avatar" />
            <input className="input-file" type="file" onChange={handleFileChange} />
            <button onClick={handleUpload}>Tải ảnh lên</button>
            <button onClick={() => setIsModalOpen(false)}>Đóng</button>
          </div>
        </div>
      )}
    </div>
  );
};

export default Sidebar;
