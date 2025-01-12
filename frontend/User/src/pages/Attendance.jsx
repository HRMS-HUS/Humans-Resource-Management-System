import React, { useState, useEffect } from 'react';
import axios from 'axios';

function Attendance() {
  const [workingDays, setWorkingDays] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchWorkingDays = async () => {
      try {
        const response = await axios.get('http://52.184.86.56:8000/api/working');
        setWorkingDays(response.data);
        setLoading(false);
      } catch (err) {
        console.error('Failed to fetch working days:', err);
        setLoading(false);
      }
    };

    fetchWorkingDays();
  }, []);

  const getStatusClass = (status) => {
    switch (status?.toLowerCase()) {
      case 'on time':
        return 'on-time';
      case 'late':
        return 'late';
      default:
        return 'absent';
    }
  };

  

  return (
    <div className="rectangle-1">
      <h1 className="page-title">Chấm công</h1>
      <table className="table">
        <thead>
          <tr>
            <th>Ngày</th>
            <th>Giờ vào</th>
            <th>Giờ ra</th>
            <th>Trạng thái</th>
          </tr>
        </thead>
        <tbody>
          {workingDays.map((day, index) => (
            <tr key={index}>
              <td>{new Date(day.date).toLocaleDateString('vi-VN')}</td>
              <td>{day.check_in_time}</td>
              <td>{day.check_out_time}</td>
              <td>
                <span className={`status ${getStatusClass(day.status)}`}>
                  {day.status === 'on time' ? 'Đúng giờ' : 
                   day.status === 'late' ? 'Đi muộn' : 'Vắng mặt'}
                </span>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default Attendance;