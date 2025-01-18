import { styled } from '@mui/material/styles';
import ArrowForwardIosSharpIcon from '@mui/icons-material/ArrowForwardIosSharp';
import MuiAccordion from '@mui/material/Accordion';
import MuiAccordionSummary, { accordionSummaryClasses } from '@mui/material/AccordionSummary';
import MuiAccordionDetails from '@mui/material/AccordionDetails';
import Typography from '@mui/material/Typography';
import AccordionActions from '@mui/material/AccordionActions';
import Button from '@mui/material/Button';
import { Box } from '@mui/material';
import { useEffect, useState } from 'react';
import { useAuthStore } from '../login/authStore';
import CircularProgress from '@mui/material/CircularProgress';
import axios from 'axios';

const Row = () => {
    const [expanded, setExpanded] = useState(false);
    const [data, setData] = useState([])
    const [isLoading, setIsLoading] = useState(false)
    const { token } = useAuthStore()

    const fetchUserInfo = async (userId) => {
        try {
            const response = await axios.get(`http://52.184.86.56:8000/api/admin/personal_info/user/${userId}`, {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            });
            return response.data.fullname;
        } catch (error) {
            console.error("Error fetching user info:", error);
            return "Unknown User";
        }
    };

    const fetchApplication = async () => {
        setIsLoading(true);
        try {
            const response = await axios.get('http://52.184.86.56:8000/api/admin/application', {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            });

            const fetchedData = response.data;

            const pendingApplications = fetchedData.filter(item => item.status === "Pending");

            const updatedData = await Promise.all(pendingApplications.map(async (item) => {
                const fullname = await fetchUserInfo(item.user_id);
                return { ...item, name: fullname };
            }));

            setData(updatedData);
        } catch (error) {
            console.error("Error fetching application:", error);
        } finally {
            setIsLoading(false);
        }
    };

    useEffect(() => {
        fetchApplication()
    }, [])

    const changeStatus = async (applicationId, status) => {
        try {
            await axios.put(`http://52.184.86.56:8000/api/admin/application/${applicationId}`, null, {
                headers: {
                    'Authorization': `Bearer ${token}`,
                },
                params: {
                    status: status,
                },
            });
            fetchApplication();
        } catch (error) {
            console.error("Error updating application status:", error);
        }
    };


    const chunkData = (arr, size) => {
        const result = [];
        for (let i = 0; i < arr.length; i += size) {
            result.push(arr.slice(i, i + size));
        }
        return result;
    };

    const displayedData = chunkData(data, 3);

    const Accordion = styled((props) => (
        <MuiAccordion disableGutters elevation={0} square {...props} />
    ))(({ theme }) => ({
        border: `1px solid ${theme.palette.divider}`,
        '&:not(:last-child)': {
            borderBottom: 0,
        },
        '&::before': {
            display: 'none',
        },
    }));

    const AccordionSummary = styled((props) => (
        <MuiAccordionSummary
            expandIcon={<ArrowForwardIosSharpIcon sx={{ fontSize: '0.9rem' }} />}
            {...props}
        />
    ))(({ theme }) => ({
        backgroundColor: 'rgba(0, 0, 0, .03)',
        flexDirection: 'row-reverse',
        [`& .${accordionSummaryClasses.expandIconWrapper}.${accordionSummaryClasses.expanded}`]:
        {
            transform: 'rotate(90deg)',
        },
        [`& .${accordionSummaryClasses.content}`]: {
            marginLeft: theme.spacing(1),
        },
        ...theme.applyStyles('dark', {
            backgroundColor: 'rgba(255, 255, 255, .05)',
        }),
    }));

    const AccordionDetails = styled(MuiAccordionDetails)(({ theme }) => ({
        padding: theme.spacing(2),
        borderTop: '1px solid rgba(0, 0, 0, .125)',
    }));

    const handleChange = (panel) => (event, newExpanded) => {
        setExpanded(newExpanded ? panel : false);
    };

    return (
        <Box sx={{ marginBottom: 2 }}>
            {isLoading ? (
                <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '200px' }}>
                    <CircularProgress />
                </Box>
            ) : (
                displayedData.map((group, groupIndex) => (
                    <Box key={groupIndex} sx={{ display: 'flex', gap: 2, marginBottom: 2 }}>
                        {group.map((item, index) => (
                            <Box key={item.application_id} sx={{ display: 'flex', flexDirection: 'column', width: '32.5%' }}>
                                <Accordion expanded={
                                    // @ts-ignore
                                    expanded === `panel${groupIndex}${index}`} onChange={handleChange(`panel${groupIndex}${index}`)}>
                                    <AccordionSummary aria-controls={`panel${groupIndex}${index}d-content`} id={`panel${groupIndex}${index}d-header`}>
                                        <Typography component="span">UserName: {item.name}</Typography>
                                    </AccordionSummary>
                                    <AccordionDetails>
                                        <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                                            <Typography>User ID: {item.user_id}</Typography>
                                            <Typography>Leave Type: {item.leave_type}</Typography>
                                            <Typography>Reason: {item.reason}</Typography>
                                            <Typography>Start Date: {item.start_date}</Typography>
                                            <Typography>End Date: {item.end_date}</Typography>
                                            <Typography>Status: {item.status}</Typography>
                                        </Box>
                                    </AccordionDetails>
                                    <AccordionActions>
                                        <Button sx={{ color: '#FF0000' }} onClick={() => changeStatus(item.application_id, 'Rejected')}>Reject</Button>
                                        <Button sx={{ color: '#33CC33' }} onClick={() => changeStatus(item.application_id, 'Approved')}>Approve</Button>
                                    </AccordionActions>
                                </Accordion>
                            </Box>
                        ))}
                    </Box>
                ))
            )}
        </Box>
    );
};

export default Row;
