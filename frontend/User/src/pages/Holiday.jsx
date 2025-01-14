import React, { useEffect, useState } from "react";
import axios from "axios";
import "../styles/Holiday.css";

function Holiday() {
  const [holidayData, setHolidayData] = useState([]);

  useEffect(() => {
    const fetchHolidays = async () => {
      try {
        const token = localStorage.getItem('token');
        const config = {
          headers: { Authorization: `Bearer ${token}` }
        };
        const response = await axios.get(`${API_URL}/me/holidays`, config);
        // sắp xếp theo ngày
        const sortedData = response.data.sort((a, b) => new Date(a.holiday_date) - new Date(b.holiday_date));
        setHolidayData(sortedData); 
      } catch (error) {
        console.error("Error fetching holidays:", error);
      }
    };

    fetchHolidays();
}, []);

  return (
    <div className="rectangle-1">
      <h1 className="page-title">Ngày lễ</h1>
      <table className="table">
        <thead>
          <tr>
            <th>Id</th>
            <th>Tên</th>
            <th>Ngày</th>
          </tr>
        </thead>
        <tbody>
          {holidayData.map((holiday) => (
            <tr key={holiday.holiday_id}>
              <td>{holiday.holiday_id}</td>
              <td>{holiday.holiday_name}</td>
              <td>{holiday.holiday_date}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default Holiday;
