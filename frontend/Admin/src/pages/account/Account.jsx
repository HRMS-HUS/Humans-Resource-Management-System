import { DataGrid, GridActionsCellItem, GridRowEditStopReasons, GridRowModes, GridToolbarContainer } from '@mui/x-data-grid';
import { initialRows } from './data';
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
import { useState } from 'react';
import { randomId } from '@mui/x-data-grid-generator';

function EditToolbar(props) {
    const { setRows, setRowModesModel } = props;

    const handleClick = () => {
        const id = randomId();
        setRows((oldRows) => [
            ...oldRows,
            { id, name: '', username: '', password: '', status: '', access: '', isNew: true }
        ]);
        setRowModesModel((oldModel) => ({
            ...oldModel,
            [id]: { mode: GridRowModes.Edit, fieldToFocus: 'name' },
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
    const [rows, setRows] = useState(initialRows);
    const [rowModesModel, setRowModesModel] = useState({});

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

    const handleDeleteClick = (id) => () => {
        setRows(rows.filter((row) => row.id !== id));
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

    const processRowUpdate = (newRow) => {
        const updatedRow = { ...newRow, isNew: false };
        setRows(rows.map((row) => (row.id === newRow.id ? updatedRow : row)));
        return updatedRow;
    };

    const handleRowModesModelChange = (newRowModesModel) => {
        setRowModesModel(newRowModesModel);
    };

    const columns = [
        { field: 'id', headerName: 'ID', width: 80, align: "center", headerAlign: "center", editable: true },
        { field: 'name', headerName: 'Full Name', flex: 1, align: "left", headerAlign: "left", editable: true },
        { field: 'username', headerName: 'Username', flex: 1, align: "left", headerAlign: "left", editable: true },
        { field: 'password', headerName: 'Password', flex: 1, align: "left", headerAlign: "left", editable: true },
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
            field: 'access', headerName: 'Access', flex: 1, align: "center", headerAlign: "center", editable: true, type: 'singleSelect', valueOptions: ['Admin', 'Manage', 'User'], renderCell: ({ row: { access } }) => {
                return (
                    <div style={{ display: "flex", justifyContent: "center", alignItems: "center", height: "100%" }}>
                        <Box sx={{
                            p: "5px",
                            width: "99px",
                            borderRadius: "3px",
                            textAlign: "center",
                            display: "flex",
                            justifyContent: "space-evenly",
                            backgroundColor: access === "Admin"
                                ? theme.palette.primary.dark
                                : access === "Manage"
                                    ? theme.palette.secondary.dark
                                    : "#3da58a"
                        }}>
                            {access === "Admin" && (<AdminPanelSettingsOutlined sx={{ color: "#fff" }} fontSize='small' />)}
                            {access === "Manage" && (<SecurityOutlined sx={{ color: "#fff" }} fontSize='small' />)}
                            {access === "User" && (<LockOpenOutlined sx={{ color: "#fff" }} fontSize='small' />)}
                            <Typography sx={{ fontSize: "13px", color: "#fff" }}> {access} </Typography>
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
        },
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
