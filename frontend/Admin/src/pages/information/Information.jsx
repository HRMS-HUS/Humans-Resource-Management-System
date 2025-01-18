import { Alert, Box, Button, MenuItem, Snackbar, TextField, Typography, useTheme } from '@mui/material';
import { DataGrid, GridActionsCellItem, GridRowEditStopReasons, GridRowModes, GridToolbar, GridToolbarContainer } from '@mui/x-data-grid';
import Header from '../../components/Header';
import { world_countries } from './data';
import Flag from 'react-world-flags';
import PersonIcon from '@mui/icons-material/Person';
import Person3Icon from '@mui/icons-material/Person3';
import Diversity3Icon from '@mui/icons-material/Diversity3';
import PersonRemoveIcon from '@mui/icons-material/PersonRemove';
import { randomId } from '@mui/x-data-grid-generator';
import PersonAddAlt1Icon from '@mui/icons-material/PersonAddAlt1';
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/DeleteOutlined';
import SaveIcon from '@mui/icons-material/Save';
import CancelIcon from '@mui/icons-material/Close';
import ImportantDevicesIcon from '@mui/icons-material/ImportantDevices';
import LockIcon from '@mui/icons-material/Lock';
import SettingsInputComponentIcon from '@mui/icons-material/SettingsInputComponent';
import CloudDownloadIcon from '@mui/icons-material/CloudDownload';
import TrendingUpIcon from '@mui/icons-material/TrendingUp';
import GroupsIcon from '@mui/icons-material/Groups';
import MonetizationOnIcon from '@mui/icons-material/MonetizationOn';
import DesignServicesIcon from '@mui/icons-material/DesignServices';
import PsychologyIcon from '@mui/icons-material/Psychology';
import GavelIcon from '@mui/icons-material/Gavel';
import SupportAgentIcon from '@mui/icons-material/SupportAgent';
import { useEffect, useState } from 'react';
import dayjs from 'dayjs';
import axios from 'axios';
import { useAuthStore } from '../login/authStore';

function EditToolbar(props) {
    const { setRows, setRowModesModel } = props;

    const handleClick = () => {
        const id = randomId();
        setRows((oldRows) => [
            ...oldRows,
            { id, user_id: '', fullname: '', citizen_card: '', department_id: '', date_of_birth: '', phone: '', email: '', marital_status: '', address: '', city: '', country: '', isNew: true }
        ]);
        setRowModesModel((oldModel) => ({
            ...oldModel,
            [id]: { mode: GridRowModes.Edit, fieldToFocus: 'user_id' },
        }));
    };

    return (
        <GridToolbarContainer>
            <Button color="primary" startIcon={<PersonAddAlt1Icon />} onClick={handleClick}>
                Add Employee
            </Button>
        </GridToolbarContainer>
    );
}

const Information = () => {

    const theme = useTheme()
    const [rows, setRows] = useState([]);
    const [rowModesModel, setRowModesModel] = useState({});
    const [loading, setLoading] = useState(null);
    const { token } = useAuthStore()
    const [snackbar, setSnackbar] = useState({ open: false, message: '', severity: 'success' });

    const fetchDepartmentInfo = async (departmentId) => {
        try {
            const response = await axios.get(`http://52.184.86.56:8000/api/admin/department/${departmentId}`, {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            });
            return response.data.department_name;
        } catch (error) {
            console.error("Error fetching department info:", error);
            return "Unknown Department";
        }
    };

    const fetchInformation = async () => {
        setLoading(true);
        try {
            const response = await axios.get('http://52.184.86.56:8000/api/admin/personal_info', {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            });
            const dataWithId = await Promise.all(response.data.map(async (item) => {
                const departmentName = await fetchDepartmentInfo(item.department_id);
                return {
                    ...item,
                    id: item.personal_info_id,
                    department_name: departmentName
                };
            }));
            setRows(dataWithId);
        } catch (error) {
            console.error("Error fetching employees:", error);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchInformation();
    }, []);

    const handleRowEditStop = (params, event) => {
        if (params.reason === GridRowEditStopReasons.rowFocusOut) {
            event.defaultMuiPrevented = true;
        }
    };

    const handleEditClick = (id) => () => {
        setRowModesModel({ ...rowModesModel, [id]: { mode: GridRowModes.Edit } });
    };

    const handleSaveClick = (id) => () => {
        setRowModesModel({ ...rowModesModel, [id]: { mode: GridRowModes.View } });
        fetchInformation();
    };

    const handleDeleteClick = (id) => async () => {
        const personal_infor_delete = rows.find((row) => row.id === id);
        const personal_info_id = personal_infor_delete.personal_info_id;

        try {
            const response = await axios.delete(`http://52.184.86.56:8000/api/admin/personal_info/${personal_info_id}`, {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            });
            if (response.status === 200) {
                setRows(rows.filter((row) => row.id !== id));
                setSnackbar({ open: true, message: 'User information deleted successfully!', severity: 'success' });
                fetchInformation();
            } else {
                console.error('Error deleting user information:', response.data);
                setSnackbar({ open: true, message: 'Failed to delete user information!', severity: 'error' });
            }
        } catch (error) {
            console.error('Error deleting user information:', error);
            setSnackbar({ open: true, message: 'Failed to delete user information!', severity: 'error' });
        }
    };

    const handleSnackbarClose = () => setSnackbar({ ...snackbar, open: false });

    const handleCancelClick = (id) => () => {
        setRowModesModel({
            ...rowModesModel,
            [id]: { mode: GridRowModes.View, ignoreModifications: true },
        });

        const editedRow = rows.find((row) => row.id === id);
        if (editedRow.isNew) {
            setRows(rows.filter((row) => row.id !== id));
        }
    };

    const processRowUpdate = async (newRow) => {
        const updatedRow = { ...newRow, isNew: false };

        try {
            const formattedStartDate = newRow.date_of_birth ? dayjs(newRow.date_of_birth).format('YYYY-MM-DD') : null;

            if (newRow.isNew) {
                const response = await axios.post('http://52.184.86.56:8000/api/admin/personal_info', null, {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    },
                    params: {
                        user_id: newRow.user_id,
                        fullname: newRow.fullname,
                        citizen_card: newRow.citizen_card,
                        department_id: newRow.department_id,
                        date_of_birth: formattedStartDate,
                        sex: newRow.sex,
                        phone: newRow.phone,
                        email: newRow.email,
                        marital_status: newRow.marital_status,
                        address: newRow.address,
                        city: newRow.city,
                        country: newRow.country,
                    }
                });
                updatedRow.user_id = response.data.user_id;
                setRows(prevRows => [...prevRows.filter(row => row.id !== updatedRow.id), updatedRow]);
                setSnackbar({ open: true, message: 'User information created successfully!', severity: 'success' });
                fetchInformation();
                return updatedRow;
            } else {
                const response = await axios.put(`http://52.184.86.56:8000/api/admin/personal_info/${newRow.personal_info_id}`, null, {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    },
                    params: {
                        user_id: newRow.user_id,
                        fullname: newRow.fullname,
                        citizen_card: newRow.citizen_card,
                        department_id: newRow.department_id,
                        date_of_birth: formattedStartDate,
                        sex: newRow.sex,
                        phone: newRow.phone,
                        email: newRow.email,
                        marital_status: newRow.marital_status,
                        address: newRow.address,
                        city: newRow.city,
                        country: newRow.country,
                    }
                });
                setSnackbar({ open: true, message: 'User information updated successfully!', severity: 'success' });
                fetchInformation();
                return updatedRow;
            }
        } catch (error) {
            console.error('Error saving data:', error.response?.data || error.message);
            setSnackbar({ open: true, message: 'Failed to save user information!', severity: 'error' });
            throw error;
        }
    };

    const handleRowModesModelChange = (newRowModesModel) => { setRowModesModel(newRowModesModel); };

    const columns = [
        { field: "user_id", headerName: "ID", width: 80, align: "center", headerAlign: "center", editable: true },
        { field: "fullname", headerName: "Full Name", cellClassName: "name-column--cell", width: 180, editable: true },
        { field: "citizen_card", headerName: "Citizen ID Number", width: 160, align: "center", headerAlign: "center", editable: true },
        { field: "department_id", headerName: "Department ID", width: 130, align: "center", headerAlign: "center", editable: true },
        {
            field: "department_name", headerName: "Department Name", width: 210, align: "center", headerAlign: "center", editable: false,
            renderCell: (params) => {
                return (
                    <Box sx={{ p: "2px", display: "flex", justifyContent: "left", alignItems: "center", height: "100%" }}>
                        {params.row.department_name === "Software Development" && (<ImportantDevicesIcon sx={{ marginRight: 1 }} fontSize='medium' />)}
                        {params.row.department_name === "CyberSecurity" && (<LockIcon sx={{ marginRight: 1 }} fontSize='medium' />)}
                        {params.row.department_name === "Hardware Development" && (<SettingsInputComponentIcon sx={{ marginRight: 1 }} fontSize='medium' />)}
                        {params.row.department_name === "Data Development" && (<CloudDownloadIcon sx={{ marginRight: 1 }} fontSize='medium' />)}
                        {params.row.department_name === "Research and Development" && (<PsychologyIcon sx={{ marginRight: 1 }} fontSize='medium' />)}
                        {params.row.department_name === "Marketing" && (<TrendingUpIcon sx={{ marginRight: 1 }} fontSize='medium' />)}
                        {params.row.department_name === "Humans Resource" && (<GroupsIcon sx={{ marginRight: 1 }} fontSize='medium' />)}
                        {params.row.department_name === "Finance" && (<MonetizationOnIcon sx={{ marginRight: 1 }} fontSize='medium' />)}
                        {params.row.department_name === "Design" && (<DesignServicesIcon sx={{ marginRight: 1 }} fontSize='medium' />)}
                        {params.row.department_name === "Legal" && (<GavelIcon sx={{ marginRight: 1 }} fontSize='medium' />)}
                        {params.row.department_name === "Customer Support" && (<SupportAgentIcon sx={{ marginRight: 1 }} fontSize='medium' />)}
                        {params.row.department_name}
                    </Box>
                )
            }
        },
        {
            field: "date_of_birth", headerName: "Date of Birth", type: "date", width: 140, align: "center", headerAlign: "center", editable: true,
            valueGetter: (params) => {
                return params?.row?.date_of_birth ? new Date(params.row.date_of_birth) : null;
            },
            renderCell: (params) => {
                const birthday = params?.row?.date_of_birth;
                return birthday ? dayjs(birthday).format('DD/MM/YYYY') : '';
            }
        },
        {
            field: "sex", headerName: "Sex", width: 120, align: "center", headerAlign: "center", editable: true, type: 'singleSelect', valueOptions: ['Male', 'Female'], renderCell: ({ row: { sex } }) => {
                return (
                    <div style={{ display: "flex", justifyContent: "center", alignItems: "center", height: "100%" }}>
                        <Box sx={{
                            p: "5px",
                            width: "99px",
                            borderRadius: "3px",
                            textAlign: "center",
                            display: "flex",
                            justifyContent: "space-evenly",
                            backgroundColor: sex === "Male" ? "#34495e" : "#16a085"
                        }}>
                            {sex === "Male" && (<PersonIcon sx={{ color: "#fff" }} fontSize='small' />)}
                            {sex === "Female" && (<Person3Icon sx={{ color: "#fff" }} fontSize='small' />)}
                            <Typography sx={{ fontSize: "13px", color: "#fff" }}> {sex} </Typography>
                        </Box>
                    </div>
                )
            }
        },
        { field: "phone", headerName: "Phone Number", width: 150, align: "center", headerAlign: "center", editable: true },
        { field: "email", headerName: "Email", width: 250, editable: true },
        {
            field: "marital_status", headerName: "Marital Status", align: "center", headerAlign: "center", width: 120, editable: true, type: 'singleSelect', valueOptions: ['Single', 'Married', 'Widowed'], renderCell: ({ row: { marital_status } }) => {
                return (
                    <div style={{ display: "flex", justifyContent: "center", alignItems: "center", height: "100%" }}>
                        <Box sx={{
                            p: "5px",
                            width: "99px",
                            borderRadius: "3px",
                            textAlign: "center",
                            display: "flex",
                            justifyContent: "space-evenly",
                            backgroundColor: marital_status === "Single"
                                ? '#ef5350'
                                : marital_status === "Married"
                                    ? '#2471a3'
                                    : "#e67e22"
                        }}>
                            {marital_status === "Single" && (<PersonIcon sx={{ color: "#fff" }} fontSize='small' />)}
                            {marital_status === "Married" && (<Diversity3Icon sx={{ color: "#fff" }} fontSize='small' />)}
                            {marital_status === "Widowed" && (<PersonRemoveIcon sx={{ color: "#fff" }} fontSize='small' />)}
                            <Typography sx={{ fontSize: "13px", color: "#fff" }}> {marital_status} </Typography>
                        </Box>
                    </div>
                )
            }
        },
        { field: "address", headerName: "Address", width: 300, editable: true },
        { field: "city", headerName: "City", width: 150, editable: true },
        {
            field: "country", headerName: "Nationality", width: 150, editable: true, type: 'singleSelect', valueOptions: world_countries.map(country => country.label).sort(),
            renderCell: ({ row: { country } }) => {
                const Country = world_countries.find(item => item.label === country)
                if (!Country) { return null }
                return (
                    <Box sx={{ display: 'flex', alignItems: 'center' }}>
                        <Flag code={Country.code} style={{ width: 20, height: 15, marginRight: 10 }} />
                        {Country.label}
                    </Box>
                );
            },
        },
        {
            field: "actions", type: "actions", headerName: "Actions", width: 100,
            getActions: ({ id }) => {
                const isRowInEditMode = rowModesModel[id]?.mode === GridRowModes.Edit;

                if (isRowInEditMode) {
                    return [
                        <GridActionsCellItem icon={<SaveIcon />} label="Save" onClick={handleSaveClick(id)} color="primary" />,
                        <GridActionsCellItem icon={<CancelIcon />} label="Cancel" onClick={handleCancelClick(id)} color="secondary" />,
                    ];
                }

                return [
                    <GridActionsCellItem icon={<EditIcon />} label="Edit" onClick={handleEditClick(id)} color="primary" />,
                    <GridActionsCellItem icon={<DeleteIcon />} label="Delete" onClick={handleDeleteClick(id)} color="error" />,
                ];
            },
        }
    ];

    return (
        <Box sx={{ height: 600, width: '98%', mx: "auto" }}>
            <Header isDashboard={false} title={undefined} subTitle={undefined} />
            <DataGrid
                rows={rows}
                // @ts-ignore
                columns={columns}
                editMode="row"
                rowModesModel={rowModesModel}
                onRowModesModelChange={handleRowModesModelChange}
                onRowEditStop={handleRowEditStop}
                processRowUpdate={processRowUpdate}
                slots={{
                    toolbar: () => (
                        <>
                            <EditToolbar setRows={setRows} setRowModesModel={setRowModesModel} />
                            <GridToolbar />
                        </>
                    ),
                }}
                checkboxSelection
                disableRowSelectionOnClick
                loading={loading}
            />
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
    );

};

export default Information;
