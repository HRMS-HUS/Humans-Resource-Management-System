import React, { useState, useEffect } from "react";
import "../styles/Dashboard.css";
import axios from "axios";

function Dashboard() {
  const [personalInfo, setPersonalInfo] = useState(null);
  const [departmentInfo, setDepartmentInfo] = useState({
    name: "",
    manager: "",
    location: "",
    mail: "",
  });
  const [jobs, setJobs] = useState([]);
  const [scheduleInfo, setScheduleInfo] = useState({
    pendingTasks: 0,
  });
  const [applicationInfo, setApplicationInfo] = useState({
    pendingApplications: 0,
    approvedApplications: 0,
  });
  const [position, setPosition] = useState("Employee");
  const [workingDays, setWorkingDays] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        const token = localStorage.getItem("token");
        const config = {
          headers: { Authorization: `Bearer ${token}` },
        };

        // Sử dụng Promise.allSettled để xử lý tất cả các request độc lập
        const [employeeRes, departmentRes, scheduleRes, applicationRes, attendanceRes] = 
          await Promise.allSettled([
            axios.get(`http://52.184.86.56:8000/api/me/personal_info`, config),
            axios.get(`http://52.184.86.56:8000/api/me/department`, config),
            axios.get(`http://52.184.86.56:8000/api/me/personal_event`, config),
            axios.get(`http://52.184.86.56:8000/api/me/application`, config),
            axios.get(`http://52.184.86.56:8000/api/me/working/history`, config)
          ]);

        // Xử lý thông tin cá nhân
        if (employeeRes.status === 'fulfilled') {
          setPersonalInfo({
            full_name: employeeRes.value.data.fullname,
            employee_id: employeeRes.value.data.user_id,
          });
        }

        // Xử lý thông tin phòng ban
        if (departmentRes.status === 'fulfilled') {
          setDepartmentInfo({
            name: departmentRes.value.data.name,
            manager: departmentRes.value.data.manager.fullname,
            location: departmentRes.value.data.location,
            mail: departmentRes.value.data.contact_email,
          });

          // Xác định chức vụ sau khi có cả thông tin nhân viên và phòng ban
          if (employeeRes.status === 'fulfilled') {
            setPosition(
              employeeRes.value.data.fullname === departmentRes.value.data.manager.fullname
                ? "Manager"
                : "Employee"
            );
          }
        }

        // Xử lý thông tin lịch
        if (scheduleRes.status === 'fulfilled') {
          const today = new Date();
          today.setHours(0, 0, 0, 0);
          
          const events = scheduleRes.value.data || [];
          const pendingTasks = events.filter((event) => {
            const startDate = new Date(event.event_start_date);
            startDate.setHours(0, 0, 0, 0);
            return startDate >= today;
          }).length;

          setScheduleInfo({
            pendingTasks: pendingTasks
          });
        }

        // Xử lý thông tin đơn
        if (applicationRes.status === 'fulfilled') {
          const applications = applicationRes.value.data || [];
          setApplicationInfo({
            pendingApplications: applications.filter(app => app.status === "Pending").length,
            approvedApplications: applications.filter(app => app.status === "Approved").length,
          });
        }

        // Xử lý thông tin chấm công
        if (attendanceRes.status === 'fulfilled') {
          const attendance = attendanceRes.value.data || [];
          const uniqueDays = new Set(attendance.map(record => record.day));
          setWorkingDays(uniqueDays.size);
        }

      } catch (error) {
        console.error("Error:", error);
        if (error.response?.status === 401) {
          useAuthStore.getState().logout();
        }
      } finally {
        setLoading(false);
      }
    };

    fetchDashboardData();
  }, []);


  return (
    <div className="rectangle-1">
      <h1 className="page-title">Overview</h1>
      <div className="dashboard">
        <div className="card">
          <h3>Personal Infomation</h3>
          <div className="info-row">
            <span>Full name : </span>
            <span>{personalInfo?.full_name || "N/A"}</span>
          </div>
          <div className="info-row">
            <span>User id : </span>
            <span>{personalInfo?.employee_id || "N/A"}</span>
          </div>
          <div className="info-row">
            <span>Department : </span>
            <span>{departmentInfo?.name || "N/A"}</span>
          </div>
          <div className="info-row">
            <span>Position : </span>
            <span>{position}</span>
          </div>
        </div>

        <div className="card">
          <h3>Statistics</h3>
          <div className="info-row">
            <span>Application for leave pending approval: </span>
            <span>{applicationInfo.pendingApplications}</span>
          </div>
          <div className="info-row">
            <span>Approved leave application: </span>
            <span>{applicationInfo.approvedApplications}</span>
          </div>
          <div className="info-row">
            <span>Mission: </span>
            <span>{scheduleInfo.pendingTasks}</span>
          </div>
          <div className="info-row">
            <span>Working days: </span>
            <span>{workingDays || 0}</span>
          </div>
        </div>
      </div>

      <div className="department-info">
        <h3>Department Information</h3>
        <div className="department-grid">
          <div className="grid_left">
            <div className="info-row">
              <span>Department name : </span>
              <span>{departmentInfo?.name || "N/A"}</span>
            </div>
            <div className="info-row">
              <span>Location : </span>
              <span>{departmentInfo?.location || "N/A"}</span>
            </div>
          </div>
          <div className="grid_right">
            <div className="info-row">
              <span>Manager : </span>
              <span>{departmentInfo?.manager || "N/A"}</span>
            </div>
            <div className="info-row">
              <span>Email : </span>
              <span>{departmentInfo?.mail || "N/A"}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;