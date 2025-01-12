import React, { useEffect, useState } from 'react';
import axios from 'axios';
import "../styles/Schedule.css";

function Schedule() {
  const [scheduleData, setScheduleData] = useState([]);

  useEffect(() => {
    const fetchSchedule = async () => {
      try {
        const response = await axios.get('http://52.184.86.56:8000/api/personal_event', {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`
          }
        });

        // Format date and time
        const formattedSchedule = response.data.map(event => {
          const formatDate = (dateString) => {
            if (!dateString) return '';
            const date = new Date(dateString);
            return date.toLocaleDateString('vi-VN');
          };

          const formatTime = (dateString) => {
            if (!dateString) return '';
            const date = new Date(dateString);
            return date.toLocaleTimeString('vi-VN', { 
              hour: '2-digit', 
              minute: '2-digit' 
            });
          };

          return {
            id: event.event_id,
            title: event.title,
            startTime: formatTime(event.start_time),
            date: formatDate(event.start_time),
            deadline: event.deadline ? 
              `${formatTime(event.deadline)} ${formatDate(event.deadline)}` : 
              ''
          };
        });

        setScheduleData(formattedSchedule);
      } catch (error) {
        console.error('Lỗi khi lấy thông tin lịch trình:', error);
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