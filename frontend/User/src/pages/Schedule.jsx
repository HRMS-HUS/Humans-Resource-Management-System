import React, { useEffect, useState } from "react";
import axios from "axios";
import "../styles/Schedule.css";

function Schedule() {
  const [scheduleData, setScheduleData] = useState([]);

  useEffect(() => {
    const fetchSchedule = async () => {
      try {
        const token = localStorage.getItem('token');
        const config = {
          headers: { Authorization: `Bearer ${token}` }
        };
        const response = await axios.get(`${API_URL}/me/personal_event`, config);

        const formattedSchedule = response.data.map((event) => ({
          id: event.event_id,
          title: event.event_title,
          startTime: new Date(event.event_start_date).toLocaleTimeString("vi-VN"),
          date: new Date(event.event_start_date).toLocaleDateString("vi-VN"),
          deadline: event.end_date
            ? new Date(event.event_end_date).toLocaleString("vi-VN")
            : null,
        }));

        setScheduleData(formattedSchedule);
      } catch (error) {
        console.error("Error fetching schedule:", error);
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
            <th>Ngày bắt đầu</th>
            <th>Ngày kết thúc</th>
          </tr>
        </thead>
        <tbody>
          {scheduleData.map((event) => (
            <tr key={event.id}>
              <td>{event.id}</td>
              <td>{event.title}</td>
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
