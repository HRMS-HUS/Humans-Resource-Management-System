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
    const fetchSalaryData = async () => {
      try {
        const response = await axios.get('http://52.184.86.56:8000/api/financial_info', {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`
          }
        });

        // Format the numbers with dots as thousand separators
        const formatNumber = (num) => {
          return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".");
        };

        setSalaryData({
          baseSalary: formatNumber(response.data.base_salary || 0),
          totalSalary: formatNumber(response.data.total_salary || 0),
          netSalary: formatNumber(response.data.net_salary || 0),
        });
      } catch (error) {
        console.error('Lỗi khi lấy thông tin lương:', error);
        // Keep the default values in case of error
      }
    };

    fetchSalaryData();
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
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>{salaryData.baseSalary}</td>
            <td>{salaryData.totalSalary}</td>
            <td>{salaryData.netSalary}</td>
          </tr>
        </tbody>
      </table>
    </div>
  );
}

export default Salary;