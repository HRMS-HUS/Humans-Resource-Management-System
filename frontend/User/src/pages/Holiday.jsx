import React, { useEffect, useState } from "react";
import axios from "axios";
import "../styles/Holiday.css";

function Holiday() {
  const [holidayData, setHolidayData] = useState([]);
  const [searchDate, setSearchDate] = useState("");
  const [filteredData, setFilteredData] = useState([]);

  useEffect(() => {
    const fetchHolidays = async () => {
      try {
        const token = localStorage.getItem("token");
        const config = {
          headers: { Authorization: `Bearer ${token}` },
        };
        const response = await axios.get(
          `http://52.184.86.56:8000/api/me/holidays`,
          config
        );

        // Sắp xếp theo ngày
        const sortedData = response.data.sort(
          (a, b) => new Date(a.holiday_date) - new Date(b.holiday_date)
        );

        setHolidayData(sortedData); // Lưu dữ liệu đã sắp xếp
        setFilteredData(sortedData); // Khởi tạo filtered data với dữ liệu đã sắp xếp
      } catch (error) {
        console.error("Error fetching holidays:", error);
      }
    };

    fetchHolidays();
  }, []);

  const handleSearch = (e) => {
    const searchValue = e.target.value;
    setSearchDate(searchValue);

    if (searchValue) {
      const filtered = holidayData.filter((holiday) =>
        holiday.holiday_date.includes(searchValue)
      );
      setFilteredData(filtered);
    } else {
      setFilteredData(holidayData);
    }
  };

  return (
    <div className="rectangle-1">
      <h1 className="page-title">Ngày lễ</h1>

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
            <th className="serial-column">STT</th>
            <th>Tên</th>
            <th>Ngày</th>
          </tr>
        </thead>
        <tbody>
          {filteredData.map((holiday, index) => (
            <tr key={holiday.holiday_id}>
              <td>{index + 1}</td> {/* Thêm số thứ tự, bắt đầu từ 1 */}
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
