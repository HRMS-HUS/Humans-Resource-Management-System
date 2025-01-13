import React, { useEffect, useState } from 'react';
import axios from 'axios';
import "../styles/Schedule.css";

function Schedule() {
  const [scheduleData, setScheduleData] = useState([]);

  useEffect(() => {
    const fetchSchedule = async () => {
        try {
            const employeeRes = await axios.get(`${API_URL}/employees/me`);
            const response = await axios.get(
                `${API_URL}/schedule/employee/${employeeRes.data.employee_id}`
            );
            
            const formattedSchedule = response.data.map(event => ({
                id: event.id,
                title: event.title,
                startTime: new Date(event.start_time).toLocaleTimeString('vi-VN'),
                date: new Date(event.start_time).toLocaleDateString('vi-VN'),
                deadline: event.deadline ? 
                    new Date(event.deadline).toLocaleString('vi-VN') : null
            }));
            
            setScheduleData(formattedSchedule);
        } catch (error) {
            console.error('Error fetching schedule:', error);
            if (error.response?.status === 401) {
                useAuthStore.getState().logout();
            }
        }
    };

    fetchSchedule();
}, []);

  return (
    <div className="rectangle-1">
      <h1 className="page-title">Lịch trình</h1>
      <table className="table">
        <thead>
          <tr>
            <th>Id</th>
            <th>Tên công việc</th>
            <th>Giờ bắt đầu</th>
            <th>Ngày</th>
            <th>Hạn công việc</th>
          </tr>
        </thead>
        <tbody>
          {scheduleData.map((event) => (
            <tr key={event.id}>
              <td>{event.id}</td>
              <td>{event.title}</td>
              <td>{event.startTime}</td>
              <td>{event.date}</td>
              <td>{event.deadline}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default Schedule;