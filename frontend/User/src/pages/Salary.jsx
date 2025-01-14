import React, { useEffect, useState } from 'react';
import axios from 'axios';
import "../styles/Salary.css";

function Salary() {
  const [salaryData, setSalaryData] = useState({
    baseSalary: '0',
    totalSalary: '0',
    netSalary: '0',
  });

  useEffect(() => {
    const fetchSalary = async () => {
        try {
            const token = localStorage.getItem('token');
            const config = {
                headers: { Authorization: `Bearer ${token}` }
            };
            const response = await axios.get(
                `${API_URL}/me/financial_info/`,
                config
            );
            
            setSalaryData({
                baseSalary: formatNumber(response.data.salaryBasic),
                totalSalary: formatNumber(response.data.salaryGross),
                netSalary: formatNumber(response.data.salaryNet)
            });
        } catch (error) {
            console.error('Error fetching salary:', error);
            if (error.response?.status === 401) {
                useAuthStore.getState().logout();
            }
        }
    };

    fetchSalary();
}, []);

  return (
    <div className="rectangle-1">
      <h1 className="page-title">Lương</h1>
      <table className="table">
        <thead>
          <tr>
            <th>Lương cơ bản</th>
            <th>Lương tổng</th>
            <th>Thực nhận</th>
            <th>Phạt</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>{salaryData.baseSalary}</td>
            <td>{salaryData.totalSalary}</td>
            <td>{salaryData.netSalary}</td>
            <td></td>
          </tr>
        </tbody>
      </table>
    </div>
  );
}

export default Salary;