import { Search, Sun, Moon, Bell } from "lucide-react";
import { useLocation } from "react-router-dom";
import { useState, useEffect } from "react";
import Badge from "@mui/material/Badge";
import axios from "axios";
import "../styles/Header.css";

function Header() {
  const location = useLocation();

  const [isDarkMode, setIsDarkMode] = useState(false);
  const [showNotifications, setShowNotifications] = useState(false);
  const [notifications, setNotifications] = useState([]);
  const [unreadCount, setUnreadCount] = useState(0);
  const [approvalMessage, setApprovalMessage] = useState(""); // Trạng thái duyệt đơn nghỉ

  const getPageName = (pathname) => {
    switch (pathname) {
      case "/":
        return "Tổng quan";
      case "/attendance":
        return "Chấm công";
      case "/schedule":
        return "Lịch trình";
      case "/salary":
        return "Lương";
      default:
        return "Tổng quan";
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
      document.body.classList.add("dark");
    } else {
      document.body.classList.remove("dark");
    }
  }, [isDarkMode]);

  // Fetch dữ liệu chuông và thông báo
  useEffect(() => {
    const fetchNotificationsAndApproval = async () => {
      try {
        const token = localStorage.getItem("token");
        const config = { headers: { Authorization: `Bearer ${token}` } };

        // Fetch trạng thái đơn nghỉ
        const approvalResponse = await axios.get(
          `http://52.184.86.56:8000/api/me/approval-status`,
          config
        );
        setApprovalMessage(
          approvalResponse.data.approved
            ? "Đơn xin nghỉ của bạn đã được duyệt!"
            : "Đơn xin nghỉ của bạn đang chờ duyệt."
        );

        // Fetch thông báo
        const response = await axios.get(
          `http://52.184.86.56:8000/api/me/notifications`,
          config
        );
        setNotifications(response.data);
        const unread = response.data.filter((notification) => !notification.read).length;
        setUnreadCount(unread);
      } catch (error) {
        console.error("Error fetching notifications:", error);
      }
    };

    fetchNotificationsAndApproval();
  }, []);

  return (
    <div className="header">
      <div className="header-left">
        <div className="breadcrumb">
          Dashboard / {getPageName(location.pathname)}
        </div>
      </div>
      <div className="header-right">
        <div className="marquee-container">
          <div className="marquee">Chào mừng đến với Hệ thống Quản lý Nhân sự</div>
        </div>
        <div className="header-icon" onClick={toggleDarkMode}>
          {isDarkMode ? <Moon size={20} /> : <Sun size={20} />}
        </div>
        <Badge
          badgeContent={unreadCount}
          color="primary"
          className="header-icon notification-icon"
          onClick={toggleNotifications}
        >
          <Bell size={20} />
          <div
            className={`notification-dropdown ${
              showNotifications ? "show" : ""
            }`}
          >
            <div className="notification-item">{approvalMessage}</div>
            {notifications.length > 0 ? (
              notifications.map((notification, index) => (
                <div
                  key={index}
                  className={`notification-item ${
                    notification.read ? "" : "unread"
                  }`}
                >
                  {notification.message}
                </div>
              ))
            ) : (
              <div className="notification-item">Không có thông báo</div>
            )}
          </div>
        </Badge>
      </div>
    </div>
  );
}

export default Header;
