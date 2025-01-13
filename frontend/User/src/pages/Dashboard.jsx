import React, { useState, useEffect } from 'react';
import '../styles/Dashboard.css';
import axios from 'axios';

function Dashboard() {
  const [personalInfo, setPersonalInfo] = useState(null);
  const [departmentInfo, setDepartmentInfo] = useState(null);
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchDashboardData = async () => {
        try {
            const token = localStorage.getItem('token');
            const config = {
                headers: { Authorization: `Bearer ${token}` }
            };
            
            // Get employee info
            const employeeRes = await axios.get(`${API_URL}/employees/me`, config);
            
            // Get department info based on employee's department_id
            const departmentRes = await axios.get(
                `${API_URL}/departments/${employeeRes.data.department_id}`, 
                config
            );
            
            // Get attendance records 
            const attendanceRes = await axios.get(
                `${API_URL}/attendance/employee/${employeeRes.data.employee_id}`,
                config
            );

            setPersonalInfo({
                full_name: employeeRes.data.full_name,
                employee_id: employeeRes.data.employee_id,
                position: employeeRes.data.position,
                join_date: employeeRes.data.join_date,
                remaining_leave_days: employeeRes.data.leave_days_remaining
            });

            setDepartmentInfo({
                name: departmentRes.data.name,
                manager_name: departmentRes.data.manager_name,
                location: departmentRes.data.location,
                employee_count: departmentRes.data.employee_count
            });

        } catch (error) {
            console.error('Error:', error);
            if (error.response?.status === 401) {
                useAuthStore.getState().logout();
            }
        }
    };

    fetchDashboardData();
}, []);
  

  const inProgressJobs = jobs.filter(job => job.status === 'in_progress').length;
  const completedJobs = jobs.filter(job => job.status === 'completed').length;

  return (
    <div className="rectangle-1">
      <h1 className="page-title">Tổng quan</h1>
      <div className="dashboard">
        <div className="card">
          <h3>Thông tin cá nhân</h3>
          <div className="info-row">
            <span>Họ và tên : </span>
            <span>{personalInfo?.full_name || 'N/A'}</span>
          </div>
          <div className="info-row">
            <span>Mã nhân viên : </span>
            <span>{personalInfo?.employee_id || 'N/A'}</span>
          </div>
          <div className="info-row">
            <span>Phòng ban : </span>
            <span>{departmentInfo?.name || 'N/A'}</span>
          </div>
          <div className="info-row">
            <span>Chức vụ : </span>
            <span>{personalInfo?.position || 'N/A'}</span>
          </div>
        </div>

        <div className="card">
          <h3>Thống kê</h3>
          <div className="info-row">
            <span>Ngày phép còn : </span>
            <span>{personalInfo?.remaining_leave_days || '0'}</span>
          </div>
          <div className="info-row">
            <span>Công việc đang làm : </span>
            <span>{inProgressJobs || '0'}</span>
          </div>
          <div className="info-row">
            <span>Công việc hoàn thành : </span>
            <span>{completedJobs || '0'}</span>
          </div>
          <div className="info-row">
            <span>Ngày vào công ty : </span>
            <span>
              {personalInfo?.join_date 
                ? new Date(personalInfo.join_date).toLocaleDateString('vi-VN')
                : 'N/A'}
            </span>
          </div>
        </div>
      </div>

      <div className="department-info">
        <h3>Thông tin phòng ban</h3>
        <div className="department-grid">
          <div className="grid_left">
            <div className="info-row">
              <span>Tên phòng : </span>
              <span>{departmentInfo?.name || 'N/A'}</span>
            </div>
            <div className="info-row">
              <span>Số lượng nhân viên : </span>
              <span>{departmentInfo?.employee_count || '0'}</span>
            </div>
          </div>
          <div className="grid_right">
            <div className="info-row">
              <span>Trưởng phòng : </span>
              <span>{departmentInfo?.manager_name || 'N/A'}</span>
            </div>
            <div className="info-row">
              <span>Vị trí : </span>
              <span>{departmentInfo?.location || 'N/A'}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;