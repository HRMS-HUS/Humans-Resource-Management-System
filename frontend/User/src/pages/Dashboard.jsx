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
  const [position, setPosition] = useState("Nhân viên");
  const [workingDays, setWorkingDays] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        const token = localStorage.getItem("token");
        const config = {
          headers: { Authorization: `Bearer ${token}` },
        };

        const employeeRes = await axios.get(
          `http://52.184.86.56:8000/api/me/personal_info`,
          config
        );
        const departmentRes = await axios.get(
          `http://52.184.86.56:8000/api/me/department`,
          config
        );
        const scheduleRes = await axios.get(
          `http://52.184.86.56:8000/api/me/personal_event`,
          config
        );
        const applicationRes = await axios.get(
          `http://52.184.86.56:8000/api/me/application`,
          config
        );

        // Xử lý dữ liệu Schedule
        const today = new Date();
        today.setHours(0, 0, 0, 0); // Đặt giờ phút giây về 0 để so sánh chính xác ngày
        const pendingTasks = scheduleRes.data.filter((event) => {
          const startDate = new Date(event.event_start_date);
          startDate.setHours(0, 0, 0, 0); // Đặt giờ phút giây về 0
          return startDate >= today; // Bao gồm cả ngày hôm nay
        }).length;

        // Xử lý dữ liệu Application
        const pendingApplications = applicationRes.data.filter(
          (app) => app.status === "Pending"
        ).length;
        const approvedApplications = applicationRes.data.filter(
          (app) => app.status === "Approved"
        ).length;

        setPersonalInfo({
          full_name: employeeRes.data.fullname,
          employee_id: employeeRes.data.user_id,
        });

        setDepartmentInfo({
          name: departmentRes.data.name,
          manager: departmentRes.data.manager.fullname, // Lấy tên từ object manager
          location: departmentRes.data.location,
          mail: departmentRes.data.contact_email,
        });

        setScheduleInfo({
          pendingTasks,
        });

        setApplicationInfo({
          pendingApplications,
          approvedApplications,
        });

        // Xử lý dữ liệu Attendance
        const attendanceRes = await axios.get(
          `http://52.184.86.56:8000/api/me/working/history`,
          config
        );
        const formattedAttendance = attendanceRes.data.map((record) => ({
          day: record.day,
        }));

        // Tính số ngày đi làm (lấy ngày duy nhất)
        const uniqueDays = new Set(formattedAttendance.map((item) => item.day));
        const totalWorkingDays = uniqueDays.size;

        setWorkingDays(totalWorkingDays);

        // Xác định chức vụ
        setPosition(employeeRes.data.fullname === departmentRes.data.manager.fullname ? "Trưởng phòng" : "Nhân viên");
      } catch (error) {
        console.error("Error:", error);
        if (error.response?.status === 401) {
          useAuthStore.getState().logout();
        }
      }
    };

    fetchDashboardData();
  }, []);

  return (
    <div className="rectangle-1">
      <h1 className="page-title">Tổng quan</h1>
      <div className="dashboard">
        <div className="card">
          <h3>Thông tin cá nhân</h3>
          <div className="info-row">
            <span>Họ và tên : </span>
            <span>{personalInfo?.full_name || "N/A"}</span>
          </div>
          <div className="info-row">
            <span>Mã nhân viên : </span>
            <span>{personalInfo?.employee_id || "N/A"}</span>
          </div>
          <div className="info-row">
            <span>Phòng ban : </span>
            <span>{departmentInfo?.name || "N/A"}</span>
          </div>
          <div className="info-row">
            <span>Chức vụ : </span>
            <span>{position}</span>
          </div>
        </div>

        <div className="card">
          <h3>Thống kê</h3>
          <div className="info-row">
            <span>Đơn xin nghỉ chờ duyệt : </span>
            <span>{applicationInfo.pendingApplications || "0"}</span>
          </div>
          <div className="info-row">
            <span>Đơn xin nghỉ đã duyệt : </span>
            <span>{applicationInfo.approvedApplications || "0"}</span>
          </div>
          <div className="info-row">
            <span>Công việc cần làm : </span>
            <span>{scheduleInfo.pendingTasks || "0"}</span>
          </div>
          <div className="info-row">
            <span>Số ngày đi làm : </span>
            <span>{workingDays || "0"}</span>
          </div>
        </div>
      </div>

      <div className="department-info">
        <h3>Thông tin phòng ban</h3>
        <div className="department-grid">
          <div className="grid_left">
            <div className="info-row">
              <span>Tên phòng : </span>
              <span>{departmentInfo?.name || "N/A"}</span>
            </div>
            <div className="info-row">
              <span>Vị trí : </span>
              <span>{departmentInfo?.location || "N/A"}</span>
            </div>
          </div>
          <div className="grid_right">
            <div className="info-row">
              <span>Trưởng phòng : </span>
              <span>{departmentInfo?.manager || "N/A"}</span>
            </div>
            <div className="info-row">
              <span>Địa chỉ mail : </span>
              <span>{departmentInfo?.mail || "N/A"}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
