import React, { useEffect, useState } from 'react';
import axios from 'axios';
import '../styles/Salary.css';
import numeral from 'numeral'; 

function Salary() {
  const [salaryData, setSalaryData] = useState({
    baseSalary: 0,
    totalAllowance: 0,
    totalSalary: 0,
    netSalary: 0,
  });

  useEffect(() => {
    const fetchSalary = async () => {
      try {
        const token = localStorage.getItem('token');
        const config = {
          headers: { Authorization: `Bearer ${token}` },
        };
        const response = await axios.get(
          `http://52.184.86.56:8000/api/me/financial_info`,
          config
        );

        const totalAllowance = Object.keys(response.data)
          .filter((key) => key.startsWith('allowance'))
          .reduce((total, key) => total + response.data[key], 0);

        setSalaryData({
          baseSalary: response.data.salaryBasic,
          totalAllowance,
          totalSalary: response.data.salaryGross,
          netSalary: response.data.salaryNet,
        });
      } catch (error) {
        console.error('Error fetching salary:', error);
        // Xử lý lỗi chi tiết hơn
      }
    };

    fetchSalary();
  }, []);

  return (
    <div className="rectangle-1">
      <h1 className="page-title">Salary</h1>
      <table className="table">
        <thead>
          <tr>
            <th>Salary basic</th>
            <th>Allowance</th>
            <th>Salary gross</th>
            <th>Salary net</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>{numeral(salaryData.baseSalary).format('0,0')}</td>
            <td>{numeral(salaryData.totalAllowance).format('0,0')}</td>
            <td>{numeral(salaryData.totalSalary).format('0,0')}</td>
            <td>{numeral(salaryData.netSalary).format('0,0')}</td>
          </tr>
        </tbody>
      </table>
    </div>
  );
}

export default Salary;