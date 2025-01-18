import Accordion from '@mui/material/Accordion';
import AccordionDetails from '@mui/material/AccordionDetails';
import AccordionSummary from '@mui/material/AccordionSummary';
import Typography from '@mui/material/Typography';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import { useEffect, useState } from 'react';
import { Stack, Box, Button, CircularProgress, Snackbar, Alert } from '@mui/material';
import NotificationAddIcon from '@mui/icons-material/NotificationAdd';
import AddAnnouncement from './AddAnnouncement';
import axios from 'axios';
import { useAuthStore } from '../login/authStore';
import Header from '../../components/Header';

const Announcement = () => {
    const [expanded, setExpanded] = useState(false);
    const [openModal, setOpenModal] = useState(false);
    const [loading, setLoading] = useState(false);
    const { token } = useAuthStore();
    const [announcementData, setAnnouncementData] = useState([]);
    const [snackbar, setSnackbar] = useState({ open: false, message: '', severity: 'success' });

    const handleChange = (panel) => (event, isExpanded) => {
        setExpanded(isExpanded ? panel : false);
    };

    const handleModalOpen = () => setOpenModal(true);
    const handleModalClose = () => setOpenModal(false);
    const handleSnackbarClose = () => setSnackbar({ ...snackbar, open: false });

    const fetchAnnouncements = async () => {
        setLoading(true);
        try {
            const [responseAnnouncement, responseDepartment] = await Promise.all([
                axios.get('http://52.184.86.56:8000/api/admin/announcement', {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                }),
                axios.get('http://52.184.86.56:8000/api/admin/department', {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                }),
            ])

            const departmentMap = responseDepartment.data.reduce((acc, dept) => {
                acc[dept.department_id] = dept.department_name;
                return acc;
            }, {});

            const announcementsWithDepartment = responseAnnouncement.data.map((announcement) => ({
                ...announcement,
                department_name: departmentMap[announcement.department_id] || 'Unknown',
            }));

            setAnnouncementData(announcementsWithDepartment);

        } catch (error) {
            console.error("Error fetching announcements:", error);
            setSnackbar({ open: true, message: 'Failed to fetch announcements.', severity: 'error' });
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchAnnouncements();
    }, []);

    const deleteAnnouncements = async (announcementId) => {
        try {
            await axios.delete(`http://52.184.86.56:8000/api/admin/announcement/${announcementId}`, {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            });
            setAnnouncementData((prevData) =>
                prevData.filter((item) => item.announcement_id !== announcementId)
            );
            setSnackbar({ open: true, message: 'Announcement deleted successfully.', severity: 'success' });
        } catch (error) {
            console.error("Error deleting announcement:", error);
            setSnackbar({ open: true, message: 'Failed to delete announcement.', severity: 'error' });
        }
    };

    return (
        <Stack direction={"column"} gap={1.5}>
            <Header title={'Announcement'} subTitle={'Manage all departments announcement'} />
            <Box sx={{ textAlign: "right", mb: 1.3 }}>
                <Button sx={{ padding: "6px 8px", textTransform: "capitalize", alignItems: "center", gap: 1 }} variant='contained' color='primary' onClick={handleModalOpen}>
                    <NotificationAddIcon />
                    Create new Announcement
                </Button>
            </Box>

            {loading ? (
                <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '200px' }}>
                    <CircularProgress />
                </Box>
            ) : (
                announcementData.map((item, index) => (
                    <Accordion
                        key={item.announcement_id}
                        // @ts-ignore
                        expanded={expanded === `panel${index}`}
                        onChange={handleChange(`panel${index}`)}
                    >
                        <AccordionSummary expandIcon={<ExpandMoreIcon />} aria-controls={`panel${index}bh-content`} id={`panel${index}bh-header`}>
                            <Typography sx={{ width: '33%', flexShrink: 0 }}>
                                Department: {item.department_id} - {item.department_name}
                            </Typography>
                            <Typography sx={{ color: 'text.secondary' }}>
                                {item.announcement_title}
                            </Typography>
                        </AccordionSummary>
                        <AccordionDetails>
                            <Typography>
                                {item.announcement_description}
                            </Typography>
                            <Box sx={{ display: 'flex', justifyContent: 'flex-end', gap: 1, mt: 2 }}>
                                <Button
                                    variant="outlined"
                                    color="error"
                                    size="small"
                                    sx={{ width: '100px' }}
                                    onClick={() => deleteAnnouncements(item.announcement_id)}
                                >
                                    Delete
                                </Button>
                            </Box>
                        </AccordionDetails>
                    </Accordion>
                ))
            )}

            <AddAnnouncement open={openModal} handleClose={handleModalClose} />

            <Snackbar
                open={snackbar.open}
                autoHideDuration={4000}
                onClose={handleSnackbarClose}
                anchorOrigin={{ vertical: 'top', horizontal: 'right' }}
            >
                <Alert onClose={handleSnackbarClose} severity={snackbar.message.includes("successfully") ? "success" : "error"} sx={{ width: '100%' }}>
                    {snackbar.message}
                </Alert>
            </Snackbar>
        </Stack>
    );
};

export default Announcement;
