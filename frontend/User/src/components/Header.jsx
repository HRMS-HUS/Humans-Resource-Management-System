import { Search, Sun, Moon, Bell } from 'lucide-react';
import { useLocation } from 'react-router-dom';
import { useState, useEffect } from 'react';
import axios from 'axios'
import '../styles/Header.css';

function Header() {
  const location = useLocation();

  const [isDarkMode, setIsDarkMode] = useState(false);
  const [showNotifications, setShowNotifications] = useState(false);

  const getPageName = (pathname) => {
    switch (pathname) {
      case '/':
        return 'Tổng quan';
      case '/attendance':
        return 'Chấm công';
      case '/schedule':
        return 'Lịch trình';
      case '/salary':
        return 'Lương';
      default:
        return 'Tổng quan';
    }
  };

  const toggleDarkMode = () => {
    setIsDarkMode((prevMode) => !prevMode);
  };

  const toggleNotifications = () => {
    setShowNotifications((prevState) => !prevState);
  };

  useEffect(() => {
    if (isDarkMode) {
      document.body.classList.add('dark');
    } else {
      document.body.classList.remove('dark');
    }
  }, [isDarkMode]);

  return (
    <div className="header">
      <div className="header-left">
        <div className="breadcrumb">
          Dashboard / {getPageName(location.pathname)}
        </div>
      </div>
      <div className="header-right">
        <div className="search-container">
          <div className="search-icon">
            <Search size={16} />
          </div>
          <input
            type="text"
            placeholder="Search"
            className="search-input"
          />
        </div>
        <div className="header-icon" onClick={toggleDarkMode}>
          {isDarkMode ? <Moon size={20} /> : <Sun size={20} />}
        </div>
        <div
          className="header-icon notification-icon"
          onClick={toggleNotifications}
        >
          <Bell size={20} />
          <div className={`notification-dropdown ${showNotifications ? 'show' : ''}`}>
            <div className="notification-item">Thông báo 1</div>
            <div className="notification-item">Thông báo 2</div>
            <div className="notification-item">Thông báo 3</div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Header;
