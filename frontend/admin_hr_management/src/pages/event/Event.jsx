import { Box, TextField, Button, Snackbar, Alert } from '@mui/material';
import axios from 'axios';
import Header from '../../components/Header';
import React, { useState } from 'react';
import { useAuthStore } from '../login/authStore';

const Event = () => {

    const { token } = useAuthStore();
    const [snackbar, setSnackbar] = useState({ open: false, message: '', severity: 'success' });
    const [loading, setLoading] = useState(false);
    const [formData, setFormData] = useState({
        user_id: '',
        event_title: '',
        event_description: '',
        event_start_date: '',
        event_end_date: '',
    });

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData({
            ...formData,
            [name]: value,
        });
    };

    const handleCreate = async (e) => {
        e.preventDefault();
        setLoading(true);
        try {
            const { user_id, event_title, event_description, event_start_date, event_end_date } = formData;

            const response = await axios.post(`http://52.184.86.56:8000/api/admin/personal_event`, null, {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
                params: {
                    user_id: user_id,
                    event_title: event_title,
                    event_description: event_description,
                    event_start_date: event_start_date,
                    event_end_date: event_end_date
                },
            });

            setSnackbar({ open: true, message: 'Event created successfully!', severity: 'success' });
            setFormData({ user_id: '', event_title: '', event_description: '', event_start_date: '', event_end_date: '' });

        } catch (error) {
            console.error('Error creating event:', error);
            setSnackbar({ open: true, message: 'Failed to create event.', severity: 'error' });
        } finally {
            setLoading(false);
        }
    };

    const handleSnackbarClose = () => {
        setSnackbar((prev) => ({ ...prev, open: false }));
    };

    return (
        <Box>
            <Header title={"Employee Events"} subTitle={"Manage all Employee Events"} />
            <Box sx={{ width: '100%', maxWidth: 700, margin: '0 auto' }}>
                <form onSubmit={handleCreate}>
                    <TextField label="User ID" name="user_id" value={formData.user_id} onChange={handleChange} fullWidth margin="normal" />
                    <TextField label="Event Title" name="event_title" value={formData.event_title} onChange={handleChange} fullWidth margin="normal" multiline minRows={1} maxRows={4} />
                    <TextField label="Event Description" name="event_description" value={formData.event_description} onChange={handleChange} fullWidth margin="normal" multiline minRows={1} maxRows={4} />
                    <TextField label="Event Start Date" name="event_start_date" value={formData.event_start_date} onChange={handleChange} fullWidth margin="normal" type="date" InputLabelProps={{ shrink: true, }} />
                    <TextField label="Event End Date" name="event_end_date" value={formData.event_end_date} onChange={handleChange} fullWidth margin="normal" type="date" InputLabelProps={{ shrink: true, }} />
                    <Box sx={{ textAlign: 'right', mb: 1.3 }}>
                        <Button
                            sx={{ padding: '6px 8px', textTransform: 'capitalize', mt: 3, width: '170px' }}
                            variant="contained"
                            color="primary"
                            onClick={handleCreate}
                            disabled={loading}
                        >
                            {loading ? 'Creating...' : 'Create Event'}
                        </Button>
                    </Box>
                </form>
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
            </Box>
        </Box>
    );
};

export default Event;
