import Backdrop from '@mui/material/Backdrop';
import Box from '@mui/material/Box';
import Modal from '@mui/material/Modal';
import Fade from '@mui/material/Fade';
import TextField from '@mui/material/TextField';
import Typography from '@mui/material/Typography';
import { useTheme } from '@mui/material';
import Button from '@mui/material/Button';
import { useState } from 'react';
import axios from 'axios';
import { useAuthStore } from '../login/authStore';
import Snackbar from '@mui/material/Snackbar';
import Alert from '@mui/material/Alert';

const style = {
    position: 'absolute',
    top: '50%',
    left: '50%',
    transform: 'translate(-50%, -50%)',
    width: 600,
    bgcolor: 'background.paper',
    border: '2px solid #000',
    boxShadow: 24,
    p: 4,
};

const AddAnnouncement = ({ open, handleClose }) => {
    
    const theme = useTheme();
    const { token } = useAuthStore();
    const [formData, setFormData] = useState({
        department_id: '',
        title: '',
        description: '',
    });
    const [snackbar, setSnackbar] = useState({ open: false, message: '', severity: 'success' });
    const [loading, setLoading] = useState(false);

    const handleInputChange = (e) => {
        const { id, value } = e.target;
        setFormData((prev) => ({ ...prev, [id]: value }));
    };

    const handleCreate = async () => {
        setLoading(true);
        try {
            const { department_id, title, description } = formData;

            const response = await axios.post(`http://52.184.86.56:8000/api/admin/announcement`, null, {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
                params: {
                    department_id: department_id,
                    announcement_title: title,
                    announcement_description: description,
                },
            });

            setSnackbar({ open: true, message: 'Announcement created successfully!', severity: 'success' });
            setFormData({ department_id: '', title: '', description: '' });
            handleClose();
        } catch (error) {
            console.error('Error creating announcement:', error);
            setSnackbar({ open: true, message: 'Failed to create announcement.', severity: 'error' });
        } finally {
            setLoading(false);
        }
    };

    const handleSnackbarClose = () => {
        setSnackbar((prev) => ({ ...prev, open: false }));
    };

    return (
        <>
            <Modal
                aria-labelledby="transition-modal-title"
                aria-describedby="transition-modal-description"
                open={open}
                onClose={handleClose}
                closeAfterTransition
                slots={{ backdrop: Backdrop }}
                slotProps={{
                    backdrop: {
                        timeout: 500,
                    },
                }}
            >
                <Fade in={open}>
                    <Box sx={style}>
                        <Typography
                            id="transition-modal-title"
                            variant="h5"
                            component="h2"
                            sx={{ textAlign: 'center', color: theme.palette.info.light, fontWeight: 'bold' }}
                        >
                            Create New Announcement
                        </Typography>
                        <TextField
                            fullWidth
                            label="Department ID"
                            id="department_id"
                            value={formData.department_id}
                            onChange={handleInputChange}
                            sx={{ mt: 4 }}
                        />
                        <TextField
                            fullWidth
                            label="Title"
                            id="title"
                            multiline
                            minRows={1}
                            maxRows={4}
                            value={formData.title}
                            onChange={handleInputChange}
                            sx={{ mt: 3 }}
                            InputProps={{ inputMode: 'text', style: { resize: 'none' } }}
                        />
                        <TextField
                            fullWidth
                            label="Description"
                            id="description"
                            multiline
                            minRows={1}
                            maxRows={4}
                            value={formData.description}
                            onChange={handleInputChange}
                            sx={{ mt: 3 }}
                            InputProps={{ inputMode: 'text', style: { resize: 'none' } }}
                        />
                        <Box sx={{ textAlign: 'right', mb: 1.3 }}>
                            <Button
                                sx={{ padding: '6px 8px', textTransform: 'capitalize', mt: 4, width: '100px' }}
                                variant="contained"
                                color="primary"
                                onClick={handleCreate}
                                disabled={loading}
                            >
                                {loading ? 'Creating...' : 'Create'}
                            </Button>
                        </Box>
                    </Box>
                </Fade>
            </Modal>
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
        </>
    );
};

export default AddAnnouncement;
