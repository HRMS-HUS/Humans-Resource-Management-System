import { Alert, Box, Button, LinearProgress, Snackbar, Typography, useTheme } from '@mui/material';
import { DataGrid, GridActionsCellItem, GridRowEditStopReasons, GridRowModes, GridToolbar, GridToolbarContainer } from '@mui/x-data-grid';
import { randomId } from '@mui/x-data-grid-generator';
import DomainAddIcon from '@mui/icons-material/DomainAdd';
import Header from '../../components/Header';
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/DeleteOutlined';
import SaveIcon from '@mui/icons-material/Save';
import CancelIcon from '@mui/icons-material/Close';
import { useEffect, useState } from 'react';
import TaskAltIcon from '@mui/icons-material/TaskAlt';
import HighlightOffIcon from '@mui/icons-material/HighlightOff';
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
import dayjs from 'dayjs';
import axios from 'axios';
import { useAuthStore } from '../login/authStore';

function EditToolbar(props) {
    const { setRows, setRowModesModel } = props;

    const handleClick = () => {
        const id = randomId();
        setRows((oldRows) => [
            ...oldRows,
            { id, department_name: '', manager_id: '', location: '', contact_email: '', email: '', start_date: new Date(), status: 'Active', isNew: true }
        ]);
        setRowModesModel((oldModel) => ({
            ...oldModel,
            [id]: { mode: GridRowModes.Edit, fieldToFocus: 'department_name' },
        }));
    };

    return (
        <GridToolbarContainer>
            <Button color="primary" startIcon={<DomainAddIcon />} onClick={handleClick}>
                Add Department
            </Button>
        </GridToolbarContainer>
    );
}

const Department = () => {
    const theme = useTheme();
    const [rows, setRows] = useState([]);
    const [rowModesModel, setRowModesModel] = useState({});
    const [loading, setLoading] = useState(false);
    const [personalInfo, setPersonalInfo] = useState([])
    const { token } = useAuthStore()
    const [snackbar, setSnackbar] = useState({ open: false, message: '', severity: 'success' });

    const fetchManagerInfo = async (managerId) => {
        try {
            const response = await axios.get(`http://52.184.86.56:8000/api/admin/users/${managerId}`, {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            });
            return response.data.username;
        } catch (error) {
            console.error("Error fetching manager info:", error);
            return "Unknown Manager";
        }
    };

    const fetchPersonalInfo = async () => {
        try {
            const response = await axios.get('http://52.184.86.56:8000/api/admin/personal_info', {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            });
            setPersonalInfo(response.data)
            const departmentCounts = response.data.reduce((acc, item) => {
                const key = item.department_id;
                acc[key] = (acc[key] || 0) + 1;
                return acc;
            }, {});
            return departmentCounts
        } catch (error) {
            console.error("Error fetching number of employee", error);
            return "Error";
        }
    };

    const fetchDepartment = async () => {
        setLoading(true);
        try {
            const [departmentsResponse, departmentCounts] = await Promise.all([
                axios.get('http://52.184.86.56:8000/api/admin/department', {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                }),
                fetchPersonalInfo(),
            ]);

            const dataWithId = await Promise.all(departmentsResponse.data.map(async (item) => {
                const managerName = await fetchManagerInfo(item.manager_id);
                return {
                    ...item,
                    id: item.department_id,
                    manager_name: managerName,
                    quantity: departmentCounts[item.department_id] || 0,
                };
            }));

            dataWithId.sort((a, b) => a.department_id.localeCompare(b.department_id));
            setRows(dataWithId);

        } catch (error) {
            console.error("Error fetching departments or employee counts:", error);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchDepartment();
    }, []);

    const handleSnackbarClose = () => setSnackbar({ ...snackbar, open: false });

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
        fetchDepartment();
    };

    const handleDeleteClick = (id) => async () => {
        const departmentToDelete = rows.find((row) => row.id === id);
        const department_id = departmentToDelete.department_id;

        try {
            const response = await axios.delete(`http://52.184.86.56:8000/api/admin/department/${department_id}`, {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            });
            if (response.status === 200) {
                setRows(rows.filter((row) => row.id !== id));
                setSnackbar({ open: true, message: 'Department deleted successfully!', severity: 'success' });
                fetchDepartment();
            } else {
                console.error('Error deleting department:', response.data);
                setSnackbar({ open: true, message: 'Failed to delete department!', severity: 'error' });
            }
        } catch (error) {
            console.error('Error deleting department:', error);
            setSnackbar({ open: true, message: 'Failed to delete department!', severity: 'error' });
        }
    };

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
            const formattedStartDate = newRow.start_date ? dayjs(newRow.start_date).format('YYYY-MM-DD') : null;

            if (newRow.isNew) {
                const response = await axios.post('http://52.184.86.56:8000/api/admin/department', null, {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    },
                    params: {
                        department_name: newRow.department_name,
                        manager_id: newRow.manager_id,
                        location: newRow.location,
                        contact_email: newRow.contact_email,
                        start_date: formattedStartDate,
                        status: newRow.status,
                    }
                });
                updatedRow.department_id = response.data.department_id;
                setRows(prevRows => [...prevRows.filter(row => row.id !== updatedRow.id), updatedRow]);
                setSnackbar({ open: true, message: 'Department created successfully!', severity: 'success' });
                fetchDepartment();
                return updatedRow;
            } else {
                const response = await axios.put(`http://52.184.86.56:8000/api/admin/department/${newRow.department_id}`, null, {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    },
                    params: {
                        department_name: newRow.department_name,
                        manager_id: newRow.manager_id,
                        location: newRow.location,
                        contact_email: newRow.contact_email,
                        start_date: formattedStartDate,
                        status: newRow.status,
                    }
                });

                setRows(rows.map((row) => (row.department_id === newRow.department_id ? updatedRow : row)));
                setSnackbar({ open: true, message: 'Department updated successfully!', severity: 'success' });
                fetchDepartment();
                return updatedRow;
            }
        } catch (error) {
            console.error('Error saving data:', error.response?.data || error.message);
            setSnackbar({ open: true, message: 'Failed to save department!', severity: 'error' });
            throw error;
        }
    };

    const handleRowModesModelChange = (newRowModesModel) => {
        setRowModesModel(newRowModesModel);
    };

    const columns = [
        { field: "department_id", headerName: "Department ID", width: 110, align: "center", headerAlign: "center", editable: true },
        {
            field: "department_name", headerName: "Department Name", width: 220, editable: true,
            renderCell: ({ row: { department_name } }) => {
                return (
                    <Box sx={{ p: "2px", display: "flex", justifyContent: "left", alignItems: "center", height: "100%" }}>
                        {department_name === "Software Development" && (<ImportantDevicesIcon sx={{ marginRight: 1 }} fontSize='medium' />)}
                        {department_name === "CyberSecurity" && (<LockIcon sx={{ marginRight: 1 }} fontSize='medium' />)}
                        {department_name === "Hardware Development" && (<SettingsInputComponentIcon sx={{ marginRight: 1 }} fontSize='medium' />)}
                        {department_name === "Data Development" && (<CloudDownloadIcon sx={{ marginRight: 1 }} fontSize='medium' />)}
                        {department_name === "Research and Development" && (<PsychologyIcon sx={{ marginRight: 1 }} fontSize='medium' />)}
                        {department_name === "Marketing" && (<TrendingUpIcon sx={{ marginRight: 1 }} fontSize='medium' />)}
                        {department_name === "Humans Resource" && (<GroupsIcon sx={{ marginRight: 1 }} fontSize='medium' />)}
                        {department_name === "Finance" && (<MonetizationOnIcon sx={{ marginRight: 1 }} fontSize='medium' />)}
                        {department_name === "Design" && (<DesignServicesIcon sx={{ marginRight: 1 }} fontSize='medium' />)}
                        {department_name === "Legal" && (<GavelIcon sx={{ marginRight: 1 }} fontSize='medium' />)}
                        {department_name === "Customer Support" && (<SupportAgentIcon sx={{ marginRight: 1 }} fontSize='medium' />)}
                        {department_name}
                    </Box>
                )
            }
        },
        { field: "manager_id", headerName: "Manager ID", width: 100, align: "center", headerAlign: "center", editable: true },
        { field: "manager_name", headerName: "Manager Name", width: 180, editable: false, align: "center", headerAlign: "center" },
        {
            field: "quantity", headerName: "Number of Employees", type: 'number', width: 180, headerAlign: "center",
            renderCell: (params) => {
                const percentage = (params.value / personalInfo.length) * 100
                return (
                    <div style={{ display: "flex", justifyContent: "flex-start", alignItems: "center", height: "100%" }}>
                        <Box sx={{ position: 'relative', height: 27, width: 100, marginRight: 1.5 }}>
                            <LinearProgress
                                variant="determinate"
                                value={percentage}
                                sx={{
                                    height: '100%',
                                    width: '100%',
                                    border: '1.75px solid',
                                    backgroundColor: theme.palette.background.default,
                                    borderColor: theme.palette.divider,
                                    '& .MuiLinearProgress-bar': {
                                        backgroundColor: percentage < 10
                                            ? "#e74c3c"
                                            : percentage >= 10 && percentage < 20
                                                ? "#33CCCC"
                                                : percentage >= 20 && percentage < 10
                                                    ? "#00CC33"
                                                    : "#607d8b",
                                    }
                                }}
                            />
                            <Box sx={{ position: 'absolute', top: '50%', left: '50%', transform: 'translate(-50%, -50%)', color: theme.palette.text.primary, fontSize: '0.9rem' }}>
                                {percentage.toFixed(2)}%
                            </Box>
                        </Box>
                        {params.value}
                    </div>
                );
            }
        },
        { field: "location", headerName: "Location", width: 250, editable: true },
        { field: "contact_email", headerName: "Contact Email", width: 250, editable: true },
        {
            field: "start_date", headerName: "Start Date", width: 120, type: "date", align: "center", headerAlign: "center", editable: true,
            valueGetter: (params) => {
                return params?.row?.start_date ? new Date(params.row.start_date) : null;
            },
            renderCell: (params) => {
                const startDate = params?.row?.start_date;
                return startDate ? dayjs(startDate).format('DD/MM/YYYY') : '';
            }
        },
        {
            field: "status",
            headerName: "Status",
            width: 120,
            align: "center",
            headerAlign: "center",
            editable: true,
            type: 'singleSelect',
            valueOptions: ['Active', 'Inactive'],
            renderCell: ({ row: { status } }) => {
                return (
                    <div style={{ display: "flex", justifyContent: "center", alignItems: "center", height: "100%" }}>
                        {status === 'Active'
                            ? <TaskAltIcon sx={{ marginRight: 1 }} fontSize='small' color="success" />
                            : <HighlightOffIcon sx={{ marginRight: 1 }} fontSize='small' color="error" />}
                        {status}
                    </div>
                )
            }
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
        },
    ];

    return (
        <Box sx={{ height: 600, width: '98%', mx: "auto" }}>
            <Header title={'Department Information'} subTitle={'Manage all departments information'} />
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
                sortModel={[
                    { field: 'department_id_suffix', sort: 'asc' },
                ]}
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
    )
}

export default Department;
