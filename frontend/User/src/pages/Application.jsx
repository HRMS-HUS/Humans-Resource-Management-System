import React, { useEffect, useState } from 'react';
import { useForm } from 'react-hook-form';
import axios from 'axios';
import '../styles/Application.css';

const Application = () => {
  const [applications, setApplications] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
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
        const token = localStorage.getItem('token');
        const config = {
          headers: { Authorization: `Bearer ${token}` },
        };
        const response = await axios.get('http://52.184.86.56:8000/api/me/application', config);
        setApplications(response.data);
      } catch (err) {
        setError('Không thể tải dữ liệu, vui lòng thử lại sau.');
      } finally {
        setLoading(false);
      }
    };

    fetchApplications();
  }, []);

  // Xử lý gửi hoặc cập nhật đơn xin nghỉ
  const onSubmit = async (data) => {
    setLoading(true);
    setError('');
    setSuccess('');

    const token = localStorage.getItem('token');
    const config = {
      headers: { Authorization: `Bearer ${token}` },
    };

    try {
      if (editingApplication) {
        // Cập nhật đơn xin nghỉ
        await axios.put(
          `http://52.184.86.56:8000/api/me/application/${editingApplication.application_id}`,
          data,
          config
        );
        setSuccess('Cập nhật đơn thành công.');
        setApplications((prev) =>
          prev.map((app) =>
            app.application_id === editingApplication.application_id
              ? { ...app, ...data }
              : app
          )
        );
      } else {
        // Gửi đơn xin nghỉ mới
        const response = await axios.post(
          'http://52.184.86.56:8000/api/me/application',
          data,
          config
        );
        setSuccess('Đơn xin nghỉ của bạn đã được gửi thành công.');
        setApplications((prev) => [...prev, response.data]);
      }
      reset();
      setEditingApplication(null);
    } catch (err) {
      setError(editingApplication ? 'Cập nhật đơn thất bại.' : 'Gửi đơn thất bại.');
    } finally {
      setLoading(false);
    }
  };

  // Hàm xóa đơn xin nghỉ
  const deleteApplication = async (id) => {
    setLoading(true);
    setError('');
    setSuccess('');

    try {
      const token = localStorage.getItem('token');
      const config = {
        headers: { Authorization: `Bearer ${token}` },
      };
      await axios.delete(`http://52.184.86.56:8000/api/me/application/${id}`, config);
      setApplications((prev) => prev.filter((app) => app.application_id !== id));
      setSuccess('Xóa đơn thành công.');
    } catch (err) {
      setError('Xóa đơn thất bại.');
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
      <h1 className="page-title">Xin nghỉ</h1>

      {/* Form gửi hoặc chỉnh sửa đơn xin nghỉ */}
      <form onSubmit={handleSubmit(onSubmit)} className="form-container">
        <div className="form-group">
          <label htmlFor="leave_type">Loại nghỉ phép</label>
          <select
            id="leave_type"
            {...register('leave_type', { required: 'Loại nghỉ phép là bắt buộc' })}
          >
            <option value="">Chọn loại nghỉ phép</option>
            <option value="Normal">Nghỉ thường</option>
            <option value="Student">Nghỉ học</option>
            <option value="Illness">Nghỉ ốm</option>
            <option value="Marriage">Nghỉ cưới</option>
          </select>
          {errors.leave_type && <p className="error">{errors.leave_type.message}</p>}
        </div>

        <div className="form-group">
          <label htmlFor="reason">Lý do</label>
          <textarea
            id="reason"
            {...register('reason', { required: 'Lý do là bắt buộc' })}
          ></textarea>
          {errors.reason && <p className="error">{errors.reason.message}</p>}
        </div>

        <div className="form-group">
          <label htmlFor="start_date">Ngày bắt đầu</label>
          <input
            type="date"
            id="start_date"
            {...register('start_date', { required: 'Ngày bắt đầu là bắt buộc' })}
          />
          {errors.start_date && <p className="error">{errors.start_date.message}</p>}
        </div>

        <div className="form-group">
          <label htmlFor="end_date">Ngày kết thúc</label>
          <input
            type="date"
            id="end_date"
            {...register('end_date', { required: 'Ngày kết thúc là bắt buộc' })}
          />
          {errors.end_date && <p className="error">{errors.end_date.message}</p>}
        </div>

        <button type="submit" className="submit-button">
          {loading ? 'Đang xử lý...' : editingApplication ? 'Cập nhật' : 'Gửi đơn'}
        </button>
      </form>

      {/* Thông báo */}
      {success && <p className="success">{success}</p>}
      {error && <p className="error">{error}</p>}

      {/* Danh sách đơn xin nghỉ */}
      <div className="applications-list">
        <h2>Danh sách đơn xin nghỉ</h2>
        {loading ? (
          <p>Đang tải dữ liệu...</p>
        ) : applications.length > 0 ? (
          <ul>
            {applications.map((app) => (
              <li key={app.application_id}>
                <p>Loại: {app.leave_type}</p>
                <p>Lý do: {app.reason}</p>
                <p>Từ: {app.start_date} - Đến: {app.end_date}</p>
                <p>Trạng thái: {app.status}</p>
                <button
                  onClick={() => editApplication(app)}
                  className="edit-button"
                >
                  Chỉnh sửa
                </button>
                <button
                  onClick={() => deleteApplication(app.application_id)}
                  className="delete-button"
                >
                  Xóa
                </button>
              </li>
            ))}
          </ul>
        ) : (
          <p>Không có đơn xin nghỉ nào.</p>
        )}
      </div>
    </div>
  );
};

export default Application;
