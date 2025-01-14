import React, { useEffect, useState } from "react";
import axios from "axios";
import "../styles/Schedule.css";

function Schedule() {
  const [scheduleData, setScheduleData] = useState([]);
  const [searchDate, setSearchDate] = useState(""); // Lưu trữ ngày tìm kiếm
  const [filteredData, setFilteredData] = useState([]); // Dữ liệu sau khi lọc
  const [formData, setFormData] = useState({
    id: null,
    title: "",
    startDate: "",
    endDate: "",
  }); // Dữ liệu form tạo hoặc chỉnh sửa
  const [isEditing, setIsEditing] = useState(false); // Trạng thái chỉnh sửa
  const [showForm, setShowForm] = useState(false); // Hiển thị form

  useEffect(() => {
    const fetchSchedule = async () => {
      try {
        const token = localStorage.getItem("token");
        const config = {
          headers: { Authorization: `Bearer ${token}` },
        };
        const response = await axios.get(
          `http://52.184.86.56:8000/api/me/personal_event`,
          config
        );

        const formattedSchedule = response.data.map((event) => ({
          id: event.event_id,
          des: event.event_description,
          title: event.event_title,
          startDate: new Date(event.event_start_date)
            .toISOString()
            .slice(0, 10),
          endDate: event.event_end_date
            ? new Date(event.event_end_date).toISOString().slice(0, 10)
            : null,
        }));

        setScheduleData(formattedSchedule);
        setFilteredData(formattedSchedule); // Set dữ liệu ban đầu
      } catch (error) {
        console.error("Error fetching schedule:", error);
        if (error.response?.status === 401) {
          useAuthStore.getState().logout();
        }
      }
    };

    fetchSchedule();
  }, []);

  // Hàm xử lý tìm kiếm theo ngày
  const handleSearch = (e) => {
    const searchValue = e.target.value;
    setSearchDate(searchValue);

    if (searchValue) {
      // Lọc dữ liệu theo ngày bắt đầu hoặc kết thúc
      const filtered = scheduleData.filter((event) => {
        return (
          event.startDate.includes(searchValue) ||
          (event.endDate && event.endDate.includes(searchValue))
        );
      });
      setFilteredData(filtered);
    } else {
      setFilteredData(scheduleData); // Nếu không nhập gì, hiển thị tất cả
    }
  };

  // Hàm xử lý khi nhấn nút "Edit"
  const handleEdit = (event) => {
    setFormData({
      id: event.id,
      des: event.event_description,
      title: event.title,
      startDate: event.startDate,
      endDate: event.endDate || "",
    });
    setIsEditing(true);
    setShowForm(true);
  };

  // Hàm xử lý khi nhấn nút "Create"
  const handleCreate = () => {
    setFormData({
      id: null,
      title: "",
      des: "",
      startDate: "",
      endDate: "",
    });
    setIsEditing(false);
    setShowForm(true);
  };

  // Hàm xử lý gửi form
  const handleSubmit = async (e) => {
    e.preventDefault();
    const token = localStorage.getItem("token");
    const config = {
      headers: { Authorization: `Bearer ${token}` },
    };

    try {
      if (isEditing) {
        // Cập nhật lịch trình
        await axios.put(
          `http://52.184.86.56:8000/api/me/personal_event/${formData.id}`,
          {
            event_title: formData.title,
            event_description: formData.des,
            event_start_date: formData.startDate,
            event_end_date: formData.endDate,
          },
          config
        );
        setScheduleData((prev) =>
          prev.map((event) =>
            event.id === formData.id
              ? {
                  ...event,
                  des: formData.des,
                  title: formData.title,
                  startDate: formData.startDate,
                  endDate: formData.endDate,
                }
              : event
          )
        );
      } else {
        // Tạo lịch trình mới
        const response = await axios.post(
          `http://52.184.86.56:8000/api/me/personal_event`,
          {
            event_title: formData.title,
            event_description: formData.des,
            event_start_date: formData.startDate,
            event_end_date: formData.endDate,
          },
          config
        );
        setScheduleData((prev) => [...prev, response.data]);
      }
      setShowForm(false);
    } catch (error) {
      console.error("Error saving schedule:", error);
    }
  };

  return (
    <div className="rectangle-1">
      <h1 className="page-title">Lịch trình</h1>

      {/* Input tìm kiếm và nút tạo lịch trình */}
      <div className="search-create-container">
        <div>
          <label htmlFor="label">Tìm theo ngày</label>
          <input
            type="date"
            value={searchDate}
            onChange={handleSearch}
            className="search-input-shedule"
            placeholder="Tìm theo ngày"
          />
        </div>
        <button onClick={handleCreate} className="create-button">
          Tạo lịch trình
        </button>
      </div>

      {/* Bảng danh sách lịch trình */}
      <table className="table">
        <thead>
          <tr>
            
            <th>Tên công việc</th>
            <th>Mô tả</th>
            <th>Ngày bắt đầu</th>
            <th>Ngày kết thúc</th>
            <th>Edit</th>
          </tr>
        </thead>
        <tbody>
          {filteredData.map((event) => (
            <tr key={event.id}>
              
              <td>{event.title}</td>
              <td>{event.des}</td>
              <td>{event.startDate}</td>
              <td>{event.endDate}</td>
              <td>
                <button
                  onClick={() => handleEdit(event)}
                  className="edit-button"
                >
                  Chỉnh sửa
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      {/* Form tạo hoặc chỉnh sửa */}
      {showForm && (
        <form onSubmit={handleSubmit} className="schedule-form">
          <div className="form-group">
            <label>Tên công việc</label>
            <input
              type="text"
              value={formData.title}
              onChange={(e) =>
                setFormData({ ...formData, title: e.target.value })
              }
              required
            />
          </div>
          <div className="form-group">
            <label>Ngày bắt đầu</label>
            <input
              type="date"
              value={formData.startDate}
              onChange={(e) =>
                setFormData({ ...formData, startDate: e.target.value })
              }
              required
            />
          </div>
          <div className="form-group">
            <label>Ngày kết thúc</label>
            <input
              type="date"
              value={formData.endDate}
              onChange={(e) =>
                setFormData({ ...formData, endDate: e.target.value })
              }
            />
          </div>
          <button type="submit" className="submit-button">
            {isEditing ? "Cập nhật" : "Tạo mới"}
          </button>
        </form>
      )}
    </div>
  );
}

export default Schedule;
