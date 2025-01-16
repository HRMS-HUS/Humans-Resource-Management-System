import React, { useState, useEffect } from "react";
import axios from "axios";
import "../styles/UserInfo.css";

function UserInfo() {
  const [userInfo, setUserInfo] = useState(null);
  const [loading, setLoading] = useState(true);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isEditMode, setIsEditMode] = useState(false);
  const [editFormData, setEditFormData] = useState({
    fullname: "",
    citizen_card: "",
    date_of_birth: "",
    sex: "",
    phone: "",
    email: "",
    marital_status: "",
    address: "",
    city: "",
    country: "",
  });

  useEffect(() => {
    const fetchUserData = async () => {
      try {
        const token = localStorage.getItem("token");
        const config = { headers: { Authorization: `Bearer ${token}` } };
        const response = await axios.get(
          "http://52.184.86.56:8000/api/me/personal_info",
          config
        );
        setUserInfo(response.data);
      } catch (error) {
        console.error("Error fetching user info:", error);
      } finally {
        setLoading(false);
      }
    };
    fetchUserData();
  }, []);

  const fieldLabels = {
    user_id: "Mã nhân viên",
    fullname: "Họ và tên",
    citizen_card: "Căn cước công dân",
    date_of_birth: "Ngày sinh",
    sex: "Giới tính",
    phone: "Số điện thoại",
    email: "Email",
    marital_status: "Tình trạng hôn nhân",
    address: "Địa chỉ",
    city: "Thành phố",
    country: "Quốc gia",
  };

  const handleEditClick = () => {
    setIsEditMode(true);
    setEditFormData({
      fullname: userInfo.fullname,
      citizen_card: userInfo.citizen_card,
      date_of_birth: userInfo.date_of_birth,
      sex: userInfo.sex,
      phone: userInfo.phone,
      email: userInfo.email,
      marital_status: userInfo.marital_status,
      address: userInfo.address,
      city: userInfo.city,
      country: userInfo.country,
    });
  };

  const handleFormChange = (e) => {
    const { name, value } = e.target;
    setEditFormData((prevData) => ({ ...prevData, [name]: value }));
  };

  const handleFormSubmit = async (e) => {
    e.preventDefault();
    try {
      const token = localStorage.getItem("token");
      const config = { headers: { Authorization: `Bearer ${token}` } };
      const queryParams = new URLSearchParams(editFormData).toString();
      const url = `http://52.184.86.56:8000/api/me/personal_info/${userInfo.personal_info_id}?${queryParams}`;
      await axios.put(url, null, config);
      setIsEditMode(false);
      setUserInfo((prevInfo) => ({ ...prevInfo, ...editFormData }));
    } catch (error) {
      console.error("Error updating user info:", error);
    }
  };

  if (loading) return <div>Loading...</div>;
  if (!userInfo) return <div>Không tìm thấy thông tin người dùng.</div>;

  return (
    <div className="rectangle1">
      <div className="user-info-container">
        <h1>Thông tin cá nhân</h1>
        <div className="user-info-card">
          <div className="user-details">
            {Object.entries(userInfo).map(([key, value]) => (
              key !== "photo_url" && (
                <div className="info-row" key={key}>
                  <strong>{fieldLabels[key] || key.replace(/_/g, " ")}:</strong> <span>{value}</span>
                </div>
              )
            ))}
          </div>
        </div>
        <button className="edit-button" onClick={handleEditClick}>
          Chỉnh sửa thông tin cá nhân
        </button>

        {isEditMode && (
          <div className="edit-form-container">
            <h2>Chỉnh sửa thông tin</h2>
            <form onSubmit={handleFormSubmit}>
              {Object.keys(editFormData).map((field) => (
                <React.Fragment key={field}>
                  <label htmlFor={field}>{fieldLabels[field] || field.replace(/_/g, " ")}</label>
                  <input
                    type={field === "date_of_birth" ? "date" : "text"}
                    name={field}
                    value={editFormData[field]}
                    onChange={handleFormChange}
                    required
                  />
                </React.Fragment>
              ))}
              <button type="submit">Lưu thay đổi</button>
            </form>
          </div>
        )}
      </div>
    </div>
  );
}

export default UserInfo;
