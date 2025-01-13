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
            const employeeRes = await axios.get(`${API_URL}/employees/me`);
            const response = await axios.get(
                `${API_URL}/payroll/employee/${employeeRes.data.employee_id}`
            );
            
            setSalaryData({
                baseSalary: formatNumber(response.data.base_salary),
                totalSalary: formatNumber(response.data.gross_salary),
                netSalary: formatNumber(response.data.net_salary)
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