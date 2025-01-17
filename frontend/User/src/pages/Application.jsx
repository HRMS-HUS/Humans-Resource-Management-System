import React, { useEffect, useState } from 'react';
import { useForm } from "react-hook-form";
import axios from "axios";
import "../styles/Application.css";

const Application = () => {
  const [applications, setApplications] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [editingApplication, setEditingApplication] = useState(null); // Lưu đơn đang được chỉnh sửa

  const {
    register,
    handleSubmit,
    formState: { errors },
    reset,
  } = useForm();

  // Lấy danh sách các đơn xin nghỉ
  useEffect(() => {
    const fetchApplications = async () => {
      setLoading(true);
      try {
        const token = localStorage.getItem("token");
        const config = {
          headers: { Authorization: `Bearer ${token}` },
        };
        const response = await axios.get(
          "http://52.184.86.56:8000/api/me/application",
          config
        );
        setApplications(response.data);
      } catch (err) {
        setError("Unable to load data, please try again later.");
      } finally {
        setLoading(false);
      }
    };

    fetchApplications();
  }, []);

  // Xử lý gửi hoặc cập nhật đơn xin nghỉ
  const onSubmit = async (data) => {
    setLoading(true);
    setError("");
    setSuccess("");

    const token = localStorage.getItem("token");
    const config = {
      headers: { Authorization: `Bearer ${token}` },
    };

    const sanitizedData = {
      user_id: "current_user_id", // Thay thế bằng user_id thực tế
      leave_type: data.leave_type || "",
      reason: data.reason || "",
      start_date: data.start_date || "",
      end_date: data.end_date || "",
      status: "Pending", // Mặc định là "Pending" nếu không gửi
    };

    try {
      if (editingApplication) {
        // Cập nhật đơn đang chỉnh sửa, sử dụng params
        const queryParams = new URLSearchParams(sanitizedData).toString();
        const response = await axios.put(
          `http://52.184.86.56:8000/api/me/application/${editingApplication.application_id}?${queryParams}`,
          null, // Không cần body vì dữ liệu nằm trong query
          config
        );

        // Cập nhật danh sách đơn
        setApplications((prev) =>
          prev.map((app) =>
            app.application_id === editingApplication.application_id
              ? response.data
              : app
          )
        );

        setSuccess("Your leave application has been successfully updated.");
      } else {
        // Tạo đơn mới, sử dụng params
        const queryParams = new URLSearchParams(sanitizedData).toString();
        const response = await axios.post(
          `http://52.184.86.56:8000/api/me/application?${queryParams}`,
          null, // Không cần body vì dữ liệu nằm trong query
          config
        );

        setSuccess("Your leave application has been submitted successfully.");
        setApplications((prev) => [...prev, response.data]);
      }

      reset();
      setEditingApplication(null);
    } catch (err) {
      setError(
        editingApplication ? "Update the application failed." : "Submit a failed application."
      );
    } finally {
      setLoading(false);
    }
  };

  // Hàm hủy chỉnh sửa
  const cancelEdit = () => {
    reset();
    setEditingApplication(null);
  };

  // Hàm xóa đơn xin nghỉ
  const deleteApplication = async (id) => {
    setLoading(true);
    setError("");
    setSuccess("");

    try {
      const token = localStorage.getItem("token");
      const config = {
        headers: { Authorization: `Bearer ${token}` },
      };
      await axios.delete(
        `http://52.184.86.56:8000/api/me/application/${id}`,
        config
      );
      setApplications((prev) =>
        prev.filter((app) => app.application_id !== id)
      );
      setSuccess("Remove successfully.");
    } catch (err) {
      setError("Remove Error.");
    } finally {
      setLoading(false);
    }
  };

  // Hàm thiết lập chỉnh sửa
  const editApplication = (application) => {
    setEditingApplication(application);
    reset(application); // Điền dữ liệu vào form
  };

  return (
    <div className="rectangle-1">
      <h1 className="page-title">Application</h1>

      {/* Form gửi hoặc chỉnh sửa đơn xin nghỉ */}
      <form onSubmit={handleSubmit(onSubmit)} className="form-container">
        <div className="form-group">
          <label htmlFor="leave_type">Leave type</label>
          <select
            id="leave_type"
            {...register("leave_type", {
              required: "Leave type is mandatory",
            })}
          >
            <option value="">Available values</option>
            <option value="Normal">Normal</option>
            <option value="Student">Student</option>
            <option value="Illness">Illness</option>
            <option value="Marriage">Marriage</option>
          </select>
          {errors.leave_type && (
            <p className="error">{errors.leave_type.message}</p>
          )}
        </div>

        <div className="form-group">
          <label htmlFor="reason">Reason</label>
          <textarea
            id="reason"
            {...register("reason", { required: "Reason is mandatory" })}
          ></textarea>
          {errors.reason && <p className="error">{errors.reason.message}</p>}
        </div>

        <div className="form-group">
          <label htmlFor="start_date">Start date</label>
          <input
            type="date"
            id="start_date"
            {...register("start_date", {
              required: "The start date is mandatory",
            })}
          />
          {errors.start_date && (
            <p className="error">{errors.start_date.message}</p>
          )}
        </div>

        <div className="form-group">
          <label htmlFor="end_date">End date</label>
          <input
            type="date"
            id="end_date"
            {...register("end_date", { required: "The end date is mandatory" })}
          />
          {errors.end_date && (
            <p className="error">{errors.end_date.message}</p>
          )}
        </div>

        <button type="submit" className="submit-button">
          {loading
            ? "Loading..."
            : editingApplication
            ? "Edit"
            : "Send"}
        </button>

        {/* Button hủy chỉnh sửa */}
        {editingApplication && (
          <button type="button" onClick={cancelEdit} className="cancel-button">
            Cancle
          </button>
        )}
      </form>

      {/* Thông báo */}
      {success && <p className="success">{success}</p>}
      {error && <p className="error">{error}</p>}

      {/* Danh sách đơn xin nghỉ */}
      <div className="applications-list">
        <h2>Application list</h2>
          {applications.length > 0 ? (
          <ul>
            {applications.map((app) => (
              <li key={app.application_id}>
                <p>Leave type: {app.leave_type}</p>
                <p>Reason: {app.reason}</p>
                <p>
                  From: {app.start_date} - To: {app.end_date}
                </p>
                <p>Status: {app.status}</p>
                <button
                  onClick={() => editApplication(app)}
                  className="edit-button"
                >
                  Edit
                </button>
                <button
                  onClick={() => deleteApplication(app.application_id)}
                  className="delete-button"
                >
                  Remove
                </button>
              </li>
            ))}
          </ul>
        ) : (
          <p>No application</p>
        )}
      </div>
    </div>
  );
};

export default Application;
