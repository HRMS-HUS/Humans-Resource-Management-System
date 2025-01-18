import { Box, CircularProgress, Paper, Typography, useTheme } from "@mui/material"
import axios from "axios";
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuthStore } from '../login/authStore';

const Notification = () => {

    const theme = useTheme()
    const [data, setData] = useState([])
    const [isLoading, setIsLoading] = useState(false)
    const { token } = useAuthStore()
    const navigate = useNavigate()

    const fetchApplication = async () => {
        setIsLoading(true);
        try {

            const [applicationResponse, personalInfoResponse] = await Promise.all([
                axios.get('http://52.184.86.56:8000/api/admin/application', {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                }),
                axios.get('http://52.184.86.56:8000/api/admin/personal_info', {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                }),
            ]);

            const fetchedApplications = applicationResponse.data;
            const fetchedPersonalInfo = personalInfoResponse.data;

            const userInfoMap = fetchedPersonalInfo.reduce((acc, user) => {
                acc[user.user_id] = user.fullname;
                return acc;
            }, {});

            const pendingApplications = fetchedApplications
                .filter((item) => item.status === "Pending")
                .map((item) => ({
                    ...item,
                    name: userInfoMap[item.user_id] || "Unknown User",
                }));

            setData(pendingApplications);
        } catch (error) {
            console.error("Error fetching application and user info:", error);
        } finally {
            setIsLoading(false);
        }
    };

    useEffect(() => {
        fetchApplication();
    }, []);

    return (
        <Box sx={{ position: 'absolute', top: 50, right: 50, width: 400, minWidth: 350, bgcolor: 'background.paper', border: '2px solid #000', borderRadius: '16px', boxShadow: 24, p: 2, maxHeight: 500, overflow: "auto", scrollbarWidth: 'none', '&::-webkit-scrollbar': { display: 'none' }, }}>
            {isLoading ? (
                <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '200px' }}>
                    <CircularProgress />
                </Box>
            ) : (
                data.map((item) => (
                    <Paper key={item.id} sx={{ mt: 1 }} onClick={() => navigate('application')}>
                        <Typography color={theme.palette.secondary.main} sx={{ padding: "3px 0 0 10px" }} variant="h6" fontWeight="600">
                            {item.name}
                        </Typography>
                        <Typography variant="h6" sx={{ padding: "1px 0 3px 10px", fontSize: "14px" }} fontWeight="400">
                            {item.reason}
                        </Typography>
                    </Paper>
                ))
            )}
        </Box>
    )
}

export default Notification
