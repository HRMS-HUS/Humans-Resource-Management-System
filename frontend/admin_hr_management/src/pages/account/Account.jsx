import { DataGrid, GridActionsCellItem, GridRowEditStopReasons, GridRowModes, GridToolbarContainer } from '@mui/x-data-grid';
import { Alert, Button, Snackbar, useTheme } from '@mui/material';
import { Box, Typography } from "@mui/material";
import { AdminPanelSettingsOutlined, LockOpenOutlined, SecurityOutlined } from '@mui/icons-material';
import TaskAltIcon from '@mui/icons-material/TaskAlt';
import HighlightOffIcon from '@mui/icons-material/HighlightOff';
import AddIcon from '@mui/icons-material/Add';
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/DeleteOutlined';
import SaveIcon from '@mui/icons-material/Save';
import CancelIcon from '@mui/icons-material/Close';
import Header from '../../components/Header'
import { useEffect, useState } from 'react';
import axios from 'axios';
import { randomId } from '@mui/x-data-grid-generator';
import { useAuthStore } from '../login/authStore';

function EditToolbar(props) {
    const { setRows, setRowModesModel } = props;

    const handleClick = () => {
        const id = randomId();
        setRows((oldRows) => [
            ...oldRows,
            { id, username: '', password: '', status: 'Active', role: 'User', isNew: true }
        ]);
        setRowModesModel((oldModel) => ({
            ...oldModel,
            [id]: { mode: GridRowModes.Edit, fieldToFocus: 'username' },
        }));
    };

    return (
        <GridToolbarContainer>
            <Button color="primary" startIcon={<AddIcon />} onClick={handleClick}>
                Add Account
            </Button>
        </GridToolbarContainer>
    );
}

const Account = () => {

    const theme = useTheme()
    const [rowModesModel, setRowModesModel] = useState({});
    const [rows, setRows] = useState([]);
    const [loading, setLoading] = useState(null);
    const [activeAccounts, setActiveAccounts] = useState([])
    const { token } = useAuthStore()
    const [snackbar, setSnackbar] = useState({ open: false, message: '', severity: 'success' })

    const fetchAccounts = async () => {
        setLoading(true);
        try {

            const response = await axios.get('http://52.184.86.56:8000/api/admin/users', {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            })

            const dataWithId = response.data.map(user => ({
                ...user,
                id: user.user_id
            }));

            setRows(dataWithId);

        } catch (error) {
            console.error("Error fetching accounts:", error);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchAccounts();
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
        fetchAccounts()
    };

    const handleDeleteClick = (id) => async () => {

        const delete_user = rows.find((row) => row.id === id)
        const user_id = delete_user.user_id

        try {
            const response = await axios.delete(`http://52.184.86.56:8000/api/admin/users/${user_id}`, {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            });
            if (response.status === 200) {
                setRows(rows.filter((row) => row.id !== id));
                setSnackbar({ open: true, message: 'Account deleted successfully!', severity: 'success' });
                fetchAccounts()
            } else {
                console.error('Error deleting account:', response.data);
                setSnackbar({ open: true, message: 'Failed to delete account!', severity: 'error' });
            }
        } catch (error) {
            console.error('Error deleting user:', error);
            setSnackbar({ open: true, message: 'Failed to delete account!', severity: 'error' });
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
            if (newRow.isNew) {
                const response = await axios.post('http://52.184.86.56:8000/api/register', null, {
                    params: {
                        username: newRow.username,
                        password: newRow.password,
                        status: newRow.status,
                        role: newRow.role,
                    }
                });
                updatedRow.user_id = response.data.user_id;
                setRows(rows.map((row) => (row.id === newRow.id ? updatedRow : row)));
                setSnackbar({ open: true, message: 'Account created successfully!', severity: 'success' });
                fetchAccounts()
                return updatedRow;
            } else {
                const response = await axios.put(`http://52.184.86.56:8000/api/admin/users/${newRow.user_id}`, null, {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    },
                    params: {
                        username: newRow.username,
                        password: newRow.password,
                        status: newRow.status,
                        role: newRow.role,
                    }
                });
                setRows(rows.map((row) => (row.id === newRow.id ? updatedRow : row)));
                setSnackbar({ open: true, message: 'Account updated successfully!', severity: 'success' });
                fetchAccounts()
                return updatedRow;
            }
        } catch (error) {
            console.error('Error saving data:', error);
            setSnackbar({ open: true, message: 'Failed to save account!', severity: 'error' });
            throw error;
        }
    };

    const handleRowModesModelChange = (newRowModesModel) => {
        setRowModesModel(newRowModesModel);
    };

    const columns = [
        { field: 'user_id', headerName: 'ID', width: 90, align: "center", headerAlign: "center", editable: true },
        { field: 'username', headerName: 'Username', width: 200, editable: true, },
        {
            field: 'password', headerName: 'Password', flex: 1, align: "center", headerAlign: "center", editable: true, renderCell: () => {
                return <Typography sx={{
                    fontSize: "13px",
                    color: "#fff",
                    fontStyle: "italic",
                    fontWeight: "bold",
                    display: "flex",
                    justifyContent: "center",
                    alignItems: "center",
                    height: "100%"
                }}>
                    Undefined
                </Typography>
            }
        },
        {
            field: 'status',
            headerName: 'Active Status',
            flex: 1,
            align: "center",
            headerAlign: "center",
            editable: true,
            type: 'singleSelect',
            valueOptions: ['Active', 'Inactive'],
            renderCell: ({ row: { status } }) => {
                return (
                    <div style={{ display: "flex", justifyContent: "center", alignItems: "center", height: "100%" }}>
                        <Box
                            sx={{
                                p: "5px",
                                width: "99px",
                                borderRadius: "3px",
                                textAlign: "center",
                                display: "flex",
                                justifyContent: "space-evenly",
                                backgroundColor: status === "Active" ? "#00C853" : "#757575",
                            }}
                        >
                            {status === "Active" && <TaskAltIcon sx={{ color: "#fff" }} fontSize="small" />}
                            {status === "Inactive" && <HighlightOffIcon sx={{ color: "#fff" }} fontSize="small" />}
                            <Typography sx={{ fontSize: "13px", color: "#fff" }}>{status}</Typography>
                        </Box>
                    </div>
                );
            },
        },
        {
            field: 'role', headerName: 'Access', flex: 1, align: "center", headerAlign: "center", editable: true, type: 'singleSelect', valueOptions: ['Admin', 'User'], renderCell: ({ row: { role } }) => {
                return (
                    <div style={{ display: "flex", justifyContent: "center", alignItems: "center", height: "100%" }}>
                        <Box sx={{
                            p: "5px",
                            width: "99px",
                            borderRadius: "3px",
                            textAlign: "center",
                            display: "flex",
                            justifyContent: "space-evenly",
                            backgroundColor: role === "Admin"
                                ? theme.palette.secondary.dark
                                : theme.palette.primary.dark
                        }}>
                            {role === "Admin" && (<AdminPanelSettingsOutlined sx={{ color: "#fff" }} fontSize='small' />)}
                            {role === "User" && (<LockOpenOutlined sx={{ color: "#fff" }} fontSize='small' />)}
                            <Typography sx={{ fontSize: "13px", color: "#fff" }}> {role} </Typography>
                        </Box>
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
        }
    ];

    return (
        <Box sx={{ height: 600, width: '100%', '& .actions': { color: 'text.secondary', }, '& .textPrimary': { color: 'text.primary', }, }}>
            <Header title={'Account'} subTitle={'Manage all employee accounts'} />
            <DataGrid
                rows={rows}
                // @ts-ignore
                columns={columns}
                editMode="row"
                rowModesModel={rowModesModel}
                onRowModesModelChange={handleRowModesModelChange}
                onRowEditStop={handleRowEditStop}
                processRowUpdate={processRowUpdate}
                slots={{ toolbar: EditToolbar }}
                slotProps={{
                    // @ts-ignore
                    toolbar: { setRows, setRowModesModel },
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
    )
}

export default Account
