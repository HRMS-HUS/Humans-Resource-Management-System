import React, { useEffect, useState } from "react";
import axios from "axios";
import "../styles/Holiday.css";

function Holiday() {
  const [holidayData, setHolidayData] = useState([]);
  const [searchDate, setSearchDate] = useState(""); // Lưu trữ ngày tìm kiếm
  const [filteredData, setFilteredData] = useState([]); // Dữ liệu sau khi lọc

  useEffect(() => {
    const fetchHolidays = async () => {
      try {
        const token = localStorage.getItem("token");
        const config = {
          headers: { Authorization: `Bearer ${token}` },
        };
        const response = await axios.get(`http://52.184.86.56:8000/api/me/holidays`, config);

        // Sắp xếp theo ngày
        const sortedData = response.data.sort(
          (a, b) => new Date(a.holiday_date) - new Date(b.holiday_date)
        );
        setHolidayData({
          holiday_id: response.data.holiday_id,
          holiday_name: response.data.holiday_name,
          holiday_date: response.data.holiday_date,
        });
        setFilteredData(response.data); // Thiết lập dữ liệu ban đầu
      } catch (error) {
        console.error("Error fetching holidays:", error);
      }
    };

    fetchHolidays();
  }, []);

  // Hàm xử lý tìm kiếm theo ngày
  const handleSearch = (e) => {
    const searchValue = e.target.value;
    setSearchDate(searchValue);

    if (searchValue) {
      // Lọc dữ liệu theo ngày
      const filtered = holidayData.filter((holiday) =>
        new Date(holiday.holiday_date).toISOString().slice(0, 10).includes(searchValue)
      );
      setFilteredData(filtered);
    } else {
      setFilteredData(holidayData); // Nếu không nhập gì, hiển thị tất cả
    }
  };

  return (
    <div className="rectangle-1">
      <h1 className="page-title">Ngày lễ</h1>

      {/* Input tìm kiếm */}
      <div className="search-create-container-holiday">
          <label htmlFor="label">Tìm theo ngày</label>
          <input
            type="date"
            value={searchDate}
            onChange={handleSearch}
            className="search-input"
            placeholder="Tìm theo ngày"
          />
        </div>

      <table className="table">
        <thead>
          <tr>
            <th>Id</th>
            <th>Tên</th>
            <th>Ngày</th>
          </tr>
        </thead>
        <tbody>
          {filteredData.map((holiday) => (
            <tr key={holiday.holiday_id}>
              <td>{holidayData.data.holiday_id}</td>
              <td>{holidayData.data.holiday_name}</td>
              <td>{holidayData.data.holiday_date}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default Holiday;
