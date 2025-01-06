import { DataGrid, GridActionsCellItem, GridRowEditStopReasons, GridRowModes, GridToolbarContainer } from '@mui/x-data-grid';
import { Button, useTheme } from '@mui/material';
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

    const fetchAccounts = async () => {
        try {
            const response = await axios.get('http://127.0.0.1:8000/api/users');
            const dataWithId = response.data.users.map(user => ({
                ...user,
                id: user.user_id
            }));
            setRows(dataWithId);
        } catch (error) {
            console.error("Error fetching accounts:", error);
        }
    };

    useEffect(() => {
        fetchAccounts()
    }, [])

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
    };

    const handleDeleteClick = (id) => async () => {

        const delete_user = rows.find((row) => row.id === id)
        const user_id = delete_user.user_id

        try {
            const response = await axios.delete(`http://127.0.0.1:8000/api/users/${user_id}`);
            if (response.status === 200) {
                setRows(rows.filter((row) => row.id !== id));
            } else {
                console.error('Error deleting user:', response.data);
            }
        } catch (error) {
            console.error('Error deleting user:', error);
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
                const response = await axios.post('http://127.0.0.1:8000/api/users', {
                    username: newRow.username,
                    password: newRow.password,
                    status: newRow.status,
                    role: newRow.role,
                });
                updatedRow.user_id = response.data.user_id;
                setRows(rows.map((row) => (row.id === newRow.id ? updatedRow : row)));
                return updatedRow;
            } else {
                const response = await axios.put(`http://127.0.0.1:8000/api/users/${newRow.user_id}`, {
                    username: newRow.username,
                    password: newRow.password,
                    status: newRow.status,
                    role: newRow.role,
                });
                setRows(rows.map((row) => (row.id === newRow.id ? updatedRow : row)));
                return updatedRow;
            }
        } catch (error) {
            console.error('Error saving data:', error);
        }
    };    

    const handleRowModesModelChange = (newRowModesModel) => {
        setRowModesModel(newRowModesModel);
    };

    const columns = [
        { field: 'user_id', headerName: 'ID', width: 120, align: "center", headerAlign: "center", editable: true },
        { field: 'username', headerName: 'Username', flex: 1, align: "left", headerAlign: "left", editable: true },
        { field: 'password', headerName: 'Password', flex: 1, align: "center", headerAlign: "center", editable: true, renderCell: () => { return 'undefined'; } },
        {
            field: 'status', headerName: 'Active Status', flex: 1, align: "center", headerAlign: "center", editable: true, type: 'singleSelect', valueOptions: ['Active', 'Inactive'], renderCell: ({ row: { status } }) => {
                return (
                    <div style={{ display: "flex", justifyContent: "center", alignItems: "center", height: "100%" }}>
                        <Box sx={{
                            p: "5px",
                            width: "99px",
                            borderRadius: "3px",
                            textAlign: "center",
                            display: "flex",
                            justifyContent: "space-evenly",
                            backgroundColor: status === "Active" ? "#00C853" : "#757575"
                        }}>
                            {status === "Active" && (<TaskAltIcon sx={{ color: "#fff" }} fontSize='small' />)}
                            {status === "Inactive" && (<HighlightOffIcon sx={{ color: "#fff" }} fontSize='small' />)}
                            <Typography sx={{ fontSize: "13px", color: "#fff" }}> {status} </Typography>
                        </Box>
                    </div>
                )
            }
        },
        {
            field: 'role', headerName: 'Access', flex: 1, align: "center", headerAlign: "center", editable: true, type: 'singleSelect', valueOptions: ['Admin', 'Manage', 'User'], renderCell: ({ row: { role } }) => {
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
                            {role === "Manage" && (<SecurityOutlined sx={{ color: "#fff" }} fontSize='small' />)}
                            {role === "User" && (<LockOpenOutlined sx={{ color: "#fff" }} fontSize='small' />)}
                            <Typography sx={{ fontSize: "13px", color: "#fff" }}> {role} </Typography>
                        </Box>
                    </div>
                )
            }
        },
        {
            field: 'actions', type: 'actions', headerName: 'Actions', width: 100, cellClassName: 'actions',
            getActions: ({ id }) => {
                const isInEditMode = rowModesModel[id]?.mode === GridRowModes.Edit;

                if (isInEditMode) {
                    return [
                        <GridActionsCellItem icon={<SaveIcon />} label="Save" sx={{ color: 'primary.main', }} onClick={handleSaveClick(id)} />,
                        <GridActionsCellItem icon={<CancelIcon />} label="Cancel" className="textPrimary" onClick={handleCancelClick(id)} color="inherit" />,
                    ];
                }

                return [
                    <GridActionsCellItem icon={<EditIcon />} label="Edit" className="textPrimary" onClick={handleEditClick(id)} color="inherit" />,
                    <GridActionsCellItem icon={<DeleteIcon />} label="Delete" onClick={handleDeleteClick(id)} color="inherit" />,
                ];
            },
        }
    ];

    return (
        <Box sx={{ height: 600, width: '100%', '& .actions': { color: 'text.secondary', }, '& .textPrimary': { color: 'text.primary', }, }}>
            <Header title={'Account'} subTitle={' '} />
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
            />
        </Box>
    )
}

export default Account
