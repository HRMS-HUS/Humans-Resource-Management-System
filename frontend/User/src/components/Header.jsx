import { Bell, Sun, Moon, X } from "lucide-react";
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
  const [selectedNotification, setSelectedNotification] = useState(null);

  const getPageName = (pathname) => {
    switch (pathname) {
      case "/":
        return "Overview";
      case "/attendance":
        return "Attendance";
      case "/schedule":
        return "Schedule";
      case "/salary":
        return "Salary";
      case "/holiday":
        return "Holiday";
      case "/application":
        return "Application";
      case "/user-info":
        return "Personal Information";
      default:
        return "Change Password";
    }
  };

  const toggleDarkMode = () => {
    setIsDarkMode((prevMode) => !prevMode);
  };

  const handleNotificationClick = (e) => {
    e.preventDefault();
    console.log("Notification clicked, current state:", !showNotifications);
    setShowNotifications((prev) => !prev);
    setSelectedNotification(null); // Reset selected notification when opening/closing dropdown
  };

  const handleNotificationItemClick = (notification) => {
    setSelectedNotification(notification);
  };

  useEffect(() => {
    if (isDarkMode) {
      document.body.classList.add("dark");
    } else {
      document.body.classList.remove("dark");
    }
  }, [isDarkMode]);

  useEffect(() => {
    const fetchNotifications = async () => {
      try {
        const token = localStorage.getItem("token");
        const config = {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        };

        const response = await axios.get(
          "http://52.184.86.56:8000/api/me/announcements",
          config
        );
        console.log("Notifications fetched:", response.data);
        setNotifications(response.data);
        setUnreadCount(response.data.length);
      } catch (error) {
        console.error("Error fetching notifications:", error);
      }
    };

    fetchNotifications();
  }, []);

  // Track notification state changes
  useEffect(() => {
    console.log("Notification state changed:", showNotifications);
  }, [showNotifications]);

  return (
    <div className="header">
      <div className="header-left">
        <div className="breadcrumb">
          Dashboard / {getPageName(location.pathname)}
        </div>
      </div>
      <div className="header-right">
        <div className="marquee-container">
          <div className="marquee">Welcome to the company</div>
        </div>
        <div className="header-icon" onClick={toggleDarkMode}>
          {isDarkMode ? <Moon size={20} /> : <Sun size={20} />}
        </div>

        {/* Notification Area */}
        <div style={{ position: "relative", display: "inline-block" }}>
          {/* Bell Icon */}
          <div
            onClick={handleNotificationClick}
            style={{
              cursor: "pointer",
              padding: "8px",
              display: "flex",
              alignItems: "center",
              position: "relative",
            }}
          >
            <Badge badgeContent={unreadCount} color="primary">
              <Bell size={20} />
            </Badge>
          </div>

          {/* Dropdown Menu */}
          {showNotifications && (
            <div
              style={{
                position: "absolute",
                top: "100%",
                right: "0",
                width: "320px",
                backgroundColor: isDarkMode ? "#333" : "#fff",
                border: "1px solid #ddd",
                borderRadius: "8px",
                boxShadow: "0 2px 10px rgba(0,0,0,0.1)",
                zIndex: 9999,
                maxHeight: "400px",
                overflowY: "auto",
                marginTop: "8px",
                color: isDarkMode ? "#fff" : "#000",
              }}
            >
              {notifications.length > 0 ? (
                <>
                  {/* Notification List */}
                  {selectedNotification ? (
                    // Description View
                    <div
                      style={{
                        padding: "16px",
                        backgroundColor: isDarkMode ? "#444" : "#fff",
                      }}
                    >
                      {/* Back button */}
                      <div
                        style={{
                          display: "flex",
                          justifyContent: "space-between",
                          alignItems: "center",
                          marginBottom: "12px",
                        }}
                      >
                        <button
                          onClick={() => setSelectedNotification(null)}
                          style={{
                            background: "none",
                            border: "1px solid",
                            color: isDarkMode ? "#fff" : "#000",
                            cursor: "pointer",
                            padding: "4px",
                            display: "flex",
                            alignItems: "center",
                            
                          }}
                        >
                          <X size={16} style={{ marginRight: "4px" }} />
                          Close
                        </button>
                      </div>
                      {/* Title */}
                      <h3
                        style={{
                          margin: "0 0 12px 0",
                          color: isDarkMode ? "#fff" : "#000",
                        }}
                      >
                        {selectedNotification.announcement_title}
                      </h3>
                      {/* Description */}
                      <p
                        style={{
                          margin: 0,
                          color: isDarkMode ? "#ddd" : "#666",
                          lineHeight: "1.5",
                        }}
                      >
                        {selectedNotification.announcement_desc}
                      </p>
                    </div>
                  ) : (
                    // List View
                    notifications.map((notification, index) => (
                      <div
                        key={index}
                        style={{
                          padding: "12px",
                          borderBottom: "1px solid #eee",
                          cursor: "pointer",
                          backgroundColor: isDarkMode ? "#444" : "#fff",
                          color: isDarkMode ? "#fff" : "#000",
                        }}
                        onClick={() => handleNotificationItemClick(notification)}
                        onMouseEnter={(e) =>
                          (e.target.style.backgroundColor = isDarkMode
                            ? "#555"
                            : "#f5f5f5")
                        }
                        onMouseLeave={(e) =>
                          (e.target.style.backgroundColor = isDarkMode
                            ? "#444"
                            : "#fff")
                        }
                      >
                        {notification.announcement_title}
                      </div>
                    ))
                  )}
                </>
              ) : (
                <div
                  style={{
                    padding: "12px",
                    textAlign: "center",
                    color: isDarkMode ? "#fff" : "#000",
                  }}
                >
                  None
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default Header;