import React, { useEffect, useState } from "react";
import axios from "axios";
import FullCalendar from "@fullcalendar/react";
import dayGridPlugin from "@fullcalendar/daygrid";
import interactionPlugin from "@fullcalendar/interaction"; // Plugin hỗ trợ sự kiện click
import "../styles/Schedule.css";

function Schedule() {
  const [events, setEvents] = useState([]); // Dữ liệu sự kiện
  const [formData, setFormData] = useState({
    id: null,
    title: "",
    description: "",
    start: "",
    end: "",
  });
  const [isEditing, setIsEditing] = useState(false);
  const [showForm, setShowForm] = useState(false);
  const [searchDate, setSearchDate] = useState(""); // New state for search input

  useEffect(() => {
    const fetchEvents = async () => {
      try {
        const token = localStorage.getItem("token");
        const config = {
          headers: { Authorization: `Bearer ${token}` },
        };
        const response = await axios.get(
          "http://52.184.86.56:8000/api/me/personal_event",
          config
        );

        const formattedEvents = response.data.map((event) => ({
          id: event.event_id,
          title: event.event_title,
          description: event.event_description,
          start: new Date(event.event_start_date).toISOString(),
          end: event.event_end_date
            ? new Date(event.event_end_date).toISOString()
            : null,
        }));

        setEvents(formattedEvents);
      } catch (error) {
        console.error("Error fetching events:", error);
      }
    };

    fetchEvents();
  }, []);

  const handleDateClick = (dateInfo) => {
    setFormData({
      id: null,
      title: "",
      description: "",
      start: dateInfo.dateStr,
      end: "",
    });
    setIsEditing(false);
    setShowForm(true);
  };

  const handleEdit = (event) => {
    setFormData({
      id: event.id,
      title: event.title,
      description: event.description,
      start: event.start.slice(0, 10),
      end: event.end ? event.end.slice(0, 10) : "",
    });
    setIsEditing(true);
    setShowForm(true);
  };

  const handleEventClick = (clickInfo) => {
    const event = events.find((e) => e.id === clickInfo.event.id);
    setFormData({
      id: event.id,
      title: event.title,
      description: event.description,
      start: event.start.slice(0, 10),
      end: event.end ? event.end.slice(0, 10) : "",
    });
    setIsEditing(true); // Không cho phép chỉnh sửa
    setShowForm(true); // Hiển thị form chỉ để xem
  };

  const deleteEvent = async (eventId) => {
    const token = localStorage.getItem("token");
    const config = {
      headers: { Authorization: `Bearer ${token}` },
    };

    try {
      await axios.delete(
        `http://52.184.86.56:8000/api/me/personal_event/${eventId}`,
        config
      );

      // Remove the event from the state after successful deletion
      setEvents((prev) => prev.filter((event) => event.id !== eventId));
    } catch (error) {
      console.error("Error deleting event:", error);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const token = localStorage.getItem("token");
    const config = {
      headers: { Authorization: `Bearer ${token}` },
    };

    try {
      const payload = {
        event_title: formData.title,
        event_description: formData.description,
        event_start_date: formData.start,
        event_end_date: formData.end || null,
      };

      if (isEditing) {
        // Đã loại bỏ PUT và không cần xử lý chỉnh sửa
      } else {
        const response = await axios.post(
          "http://52.184.86.56:8000/api/me/personal_event",
          null,
          { ...config, params: payload }
        );

        const newEvent = {
          id: response.data.event_id,
          title: formData.title,
          description: formData.description,
          start: formData.start,
          end: formData.end,
        };

        setEvents((prev) => [...prev, newEvent]);
      }

      setShowForm(false);
    } catch (error) {
      console.error("Error saving event:", error);
    }
  };
  const handleRowClick = (event) => {
    setFormData({
      id: event.id,
      title: event.title,
      description: event.description,
      start: event.start.slice(0, 10),
      end: event.end ? event.end.slice(0, 10) : "",
    });
    setIsEditing(true); // Cho phép xem chi tiết (nếu cần chỉnh sửa sau)
    setShowForm(true); // Hiển thị form
  };

  const handleSearch = (e) => {
    setSearchDate(e.target.value);
  };

  const filteredEvents = searchDate
    ? events.filter(
        (event) =>
          event.start.startsWith(searchDate) ||
          event.end?.startsWith(searchDate)
      )
    : events;

  return (
    <div className="rectangle1">
      <div className="schedule-container">
        <h1>Lịch trình</h1>

        <FullCalendar
          plugins={[dayGridPlugin, interactionPlugin]}
          initialView="dayGridMonth"
          events={events}
          dateClick={handleDateClick}
          eventClick={handleEventClick}
          height="auto"
          dayCellContent={(dayCell) => (
            <div>{dayCell.date.getDate()}</div> // Đảm bảo nội dung ngày không bị giãn
          )}
        />
        {/* Bảng danh sách lịch trình */}
        <div className="schedule-list">
          <h2>Danh sách lịch trình</h2>
          {/* Search section */}
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
          </div>

          <table className="table">
            <thead>
              <tr>
                <th>Tên công việc</th>
                <th>Mô tả</th>
                <th>Ngày bắt đầu</th>
                <th>Ngày kết thúc</th>
                <th>Xóa lịch</th>
              </tr>
            </thead>
            <tbody>
              {filteredEvents.map((event) => (
                <tr
                  key={event.id}
                  onClick={() => handleRowClick(event)} // Thêm sự kiện click
                  className="clickable-row"
                >
                  <td>{event.title}</td>
                  <td>{event.description}</td>
                  <td>{new Date(event.start).toLocaleDateString()}</td>
                  <td>
                    {event.end ? new Date(event.end).toLocaleDateString() : "-"}
                  </td>
                  <td>
                    <button
                      onClick={(e) => {
                        e.stopPropagation(); // Ngăn sự kiện click dòng
                        deleteEvent(event.id);
                      }}
                      className="edit-button"
                    >
                      Xóa
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        {showForm && (
          <form onSubmit={handleSubmit} className="schedule-form">
            <div>
              <label>Tiêu đề</label>
              <input
                type="text"
                value={formData.title}
                onChange={(e) =>
                  setFormData({ ...formData, title: e.target.value })
                }
                required
              />
            </div>
            <div>
              <label>Mô tả</label>
              <textarea
                value={formData.description}
                onChange={(e) =>
                  setFormData({ ...formData, description: e.target.value })
                }
                required
              />
            </div>
            <div>
              <label>Ngày bắt đầu</label>
              <input
                type="date"
                value={formData.start}
                onChange={(e) =>
                  setFormData({ ...formData, start: e.target.value })
                }
                required
              />
            </div>
            <div>
              <label>Ngày kết thúc</label>
              <input
                type="date"
                value={formData.end}
                onChange={(e) =>
                  setFormData({ ...formData, end: e.target.value })
                }
              />
            </div>
            {!isEditing && <button type="submit">Tạo mới</button>}
            <button
              type="button"
              className="close-button"
              onClick={() => setShowForm(false)}
            >
              Đóng
            </button>
          </form>
        )}
      </div>
    </div>
  );
}

export default Schedule;
