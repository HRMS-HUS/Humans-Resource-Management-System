import React, { useState, useEffect } from 'react';
import axios from 'axios';

function Attendance() {
  const [workingDays, setWorkingDays] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchAttendance = async () => {
      try {
        const token = localStorage.getItem('token');
        const config = {
          headers: { Authorization: `Bearer ${token}` },
        };

        const response = await axios.get(
          `http://52.184.86.56:8000/api/me/working/history`,
          config
        );

        const formattedAttendance = response.data
          .map((record) => ({
            working_id: record.working_id,
            day: record.day,
            login_time: record.login_time,
            logout_time: record.logout_time,
            total_hours: record.total_hours.toFixed(2),
          }))
          .sort((a, b) => new Date(b.day) - new Date(a.day));

        setWorkingDays(formattedAttendance);
      } catch (error) {
        console.error('Error fetching attendance:', error);
        if (error.response?.status === 401) {
          useAuthStore.getState().logout();
        }
      } finally {
        setLoading(false);
      }
    };

    fetchAttendance();
  }, []);

  const formatDate = (dateString) => {
    if (!dateString) return 'Không có';
    const date = new Date(dateString);
    return date.toLocaleDateString('vi-VN', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
    });
  };

  const formatTime = (timeString) => {
    if (!timeString) return 'Không có';
    const [timePart] = timeString.split('+'); // Loại bỏ múi giờ (+00:00)
    const time = new Date(`1970-01-01T${timePart}`);
    return new Intl.DateTimeFormat('vi-VN', {
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit',
      hour12: false,
    }).format(time);
  };

  return (
    <div className="rectangle-1">
      <h1 className="page-title">Lịch sử</h1>
      <table className="table">
        <thead>
          <tr>
            <th>Ngày</th>
            <th>Giờ vào</th>
            <th>Giờ ra</th>
            <th>Số giờ làm việc</th>
          </tr>
        </thead>
        <tbody>
          {workingDays.map((record) => (
            <tr key={record.working_id}>
              <td>{formatDate(record.day)}</td>
              <td>{formatTime(record.login_time)}</td>
              <td>{formatTime(record.logout_time)}</td>
              <td>{record.total_hours}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default Attendance;
