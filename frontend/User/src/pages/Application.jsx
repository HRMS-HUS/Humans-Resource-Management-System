import React, { useEffect, useState } from 'react';
import { useForm } from 'react-hook-form';
import axios from 'axios';
import '../styles/Application.css';

const Application = () => {
  const [applications, setApplications] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

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

  // Xử lý gửi đơn xin nghỉ
  const onSubmit = async (data) => {
    setLoading(true);
    setError('');
    setSuccess('');
    try {
      const token = localStorage.getItem('token');
      const config = {
        headers: { Authorization: `Bearer ${token}` },
      };
      // Gửi đơn xin nghỉ
      const response = await axios.post('http://52.184.86.56:8000/api/me/application', data, config);
      setSuccess('Đơn xin nghỉ của bạn đã được gửi thành công.');
      setApplications((prev) => [...prev, response.data]);
      reset();
    } catch (err) {
      setError('Gửi đơn thất bại, vui lòng thử lại.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="rectangle-1">
      <h1 className="page-title">Xin nghỉ</h1>

      {/* Form gửi đơn xin nghỉ */}
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
          {loading ? 'Đang gửi...' : 'Gửi đơn'}
        </button>
      </form>

      {/* Thông báo thành công hoặc lỗi */}
      {success && <p className="success">{success}</p>}
      {error && <p className="error">{error}</p>}
      
      {/* Hiển thị danh sách đơn xin nghỉ */}
      <div className="applications-list">
        <h2>Danh sách đơn xin nghỉ</h2>
        {loading ? (
          <p>Đang tải dữ liệu...</p>
        ) : error ? (
          <p className="error">{error}</p>
        ) : applications.length > 0 ? (
          <ul>
            {applications.map((app, index) => (
              <li key={index}>
                <p>Loại: {app.leave_type}</p>
                <p>Lý do: {app.reason}</p>
                <p>Từ: {app.start_date} - Đến: {app.end_date}</p>
                <p>Trạng thái: {app.status}</p>
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
