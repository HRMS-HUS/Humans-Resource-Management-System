import { Stack, useTheme } from '@mui/material';
import Card from './Card';
import GroupsIcon from '@mui/icons-material/Groups';
import BusinessIcon from '@mui/icons-material/Business';
import MonetizationOnIcon from '@mui/icons-material/MonetizationOn';
import ArticleIcon from '@mui/icons-material/Article';
import { useState, useEffect } from 'react';
import axios from 'axios';
import { useAuthStore } from '../login/authStore';
import { useNavigate } from 'react-router-dom';

const Row1 = () => {
    const theme = useTheme();
    const [employees, setEmployees] = useState([]);
    const [salary, setSalary] = useState([]);
    const [departments, setDepartments] = useState([]);
    const [application, setApplication] = useState([]);
    const { token } = useAuthStore();
    const navigate = useNavigate()

    useEffect(() => {
        const fetchData = async () => {
            try {
                const [accountsResponse, financialResponse, departmentResponse, applicationResponse] = await Promise.all([
                    axios.get('http://52.184.86.56:8000/api/admin/users', {
                        headers: {
                            Authorization: `Bearer ${token}`,
                        },
                    }),
                    axios.get('http://52.184.86.56:8000/api/admin/financial_info', {
                        headers: {
                            Authorization: `Bearer ${token}`,
                        },
                    }),
                    axios.get('http://52.184.86.56:8000/api/admin/department', {
                        headers: {
                            Authorization: `Bearer ${token}`,
                        },
                    }),
                    axios.get('http://52.184.86.56:8000/api/admin/application', {
                        headers: {
                            Authorization: `Bearer ${token}`,
                        },
                    })
                ]);
                setEmployees(accountsResponse.data);
                setSalary(financialResponse.data.map(item => item.salaryNet));
                setDepartments(departmentResponse.data);
                const pendingApplications = applicationResponse.data.filter(item => item.status === "Pending");
                setApplication(pendingApplications);

            } catch (error) {
                console.error("Error fetching data:", error);
            }
        };

        fetchData();
    }, [token]);

    return (
        <Stack direction={"row"} flexWrap={"wrap"} gap={1} justifyContent={{ xs: 'center', sm: "space-between" }}>
            <Card
                icon={<GroupsIcon sx={{ fontSize: '80px', color: theme.palette.secondary.main }} />}
                title={'Employees'}
                subTitle={employees.length}
            />

            <Card
                icon={<MonetizationOnIcon sx={{ fontSize: "80px", color: theme.palette.secondary.main }} />}
                title={'Total Salary'}
                subTitle={((salary.reduce((sum, current) => sum + current, 0)).toLocaleString())}
            />

            <Card
                icon={<BusinessIcon sx={{ fontSize: "80px", color: theme.palette.secondary.main }} />}
                title={'Departments'}
                subTitle={departments.length}
            />

            <Card
                icon={<ArticleIcon sx={{ fontSize: '80px', color: theme.palette.secondary.main }} />}
                title={'Application'}
                subTitle={application.length}
            />
        </Stack>
    );
}

export default Row1;
