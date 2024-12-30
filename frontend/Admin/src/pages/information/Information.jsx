import { Box, Button, MenuItem, TextField, Typography, useTheme } from '@mui/material';
import { DataGrid, GridActionsCellItem, GridRowEditStopReasons, GridRowModes, GridToolbar, GridToolbarContainer } from '@mui/x-data-grid';
import Header from '../../components/Header';
import { initialRows, world_countries } from './data';
import Flag from 'react-world-flags';
import PersonIcon from '@mui/icons-material/Person';
import Person3Icon from '@mui/icons-material/Person3';
import Diversity3Icon from '@mui/icons-material/Diversity3';
import PersonRemoveIcon from '@mui/icons-material/PersonRemove';
import { randomId } from '@mui/x-data-grid-generator';
import AddIcon from '@mui/icons-material/Add';
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/DeleteOutlined';
import SaveIcon from '@mui/icons-material/Save';
import CancelIcon from '@mui/icons-material/Close';
import { useState } from 'react';

function EditToolbar(props) {
    const { setRows, setRowModesModel } = props;

    const handleClick = () => {
        const id = randomId();
        setRows((oldRows) => [
            ...oldRows,
            { id, name: '', citizen: '', birthday: '', phone: '', email: '', marital: '', address: '', city: '', country: '', isNew: true }
        ]);
        setRowModesModel((oldModel) => ({
            ...oldModel,
            [id]: { mode: GridRowModes.Edit, fieldToFocus: 'name' },
        }));
    };

    return (
        <GridToolbarContainer>
            <Button color="primary" startIcon={<AddIcon />} onClick={handleClick}>
                Add Employee
            </Button>
        </GridToolbarContainer>
    );
}

const Information = () => {

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
        { field: "id", headerName: "ID", width: 80, align: "center", headerAlign: "center", editable: true },
        { field: "name", headerName: "Full Name", cellClassName: "name-column--cell", width: 200, editable: true },
        { field: "citizen", headerName: "Citizen ID Number", width: 160, editable: true },
        { field: "birthday", headerName: "Date of Birth", type: "date", width: 140, editable: true },
        {
            field: "sex", headerName: "Sex", width: 110, align: "center", headerAlign: "center", editable: true, type: 'singleSelect', valueOptions: ['Male', 'Female'], renderCell: ({ row: { sex } }) => {
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
        { field: "phone", headerName: "Phone Number", width: 150, editable: true },
        { field: "email", headerName: "Email", width: 250, editable: true },
        {
            field: "marital", headerName: "Marital Status", align: "center", headerAlign: "center", width: 120, editable: true, type: 'singleSelect', valueOptions: ['Single', 'Married', 'Widowed'], renderCell: ({ row: { marital } }) => {
                return (
                    <div style={{ display: "flex", justifyContent: "center", alignItems: "center", height: "100%" }}>
                        <Box sx={{
                            p: "5px",
                            width: "99px",
                            borderRadius: "3px",
                            textAlign: "center",
                            display: "flex",
                            justifyContent: "space-evenly",
                            backgroundColor: marital === "Single"
                                ? '#ef5350'
                                : marital === "Married"
                                    ? '#2471a3'
                                    : "#e67e22"
                        }}>
                            {marital === "Single" && (<PersonIcon sx={{ color: "#fff" }} fontSize='small' />)}
                            {marital === "Married" && (<Diversity3Icon sx={{ color: "#fff" }} fontSize='small' />)}
                            {marital === "Widowed" && (<PersonRemoveIcon sx={{ color: "#fff" }} fontSize='small' />)}
                            <Typography sx={{ fontSize: "13px", color: "#fff" }}> {marital} </Typography>
                        </Box>
                    </div>
                )
            }
        },
        { field: "address", headerName: "Address", width: 270, editable: true },
        { field: "city", headerName: "City", width: 150, editable: true },
        {
            field: "country", headerName: "Country", width: 160, editable: true, type: 'singleSelect', valueOptions: world_countries.map(country => country.label),
            renderCell: (params) => {
                const countryLabel = params.value
                const country = world_countries.find(item => item.label === countryLabel)
                if (!country) { return null }
                return (
                    <Box sx={{ display: 'flex', alignItems: 'center' }}>
                        <Flag code={country.code} style={{ width: 20, height: 15, marginRight: 10 }} />
                        {country.label}
                    </Box>
                );
            },
            renderEditCell: (params) => {
                const country = world_countries.find(item => item.label === params.value);
                return (
                    <TextField
                        type="text"
                        value={country ? country.label : ''}
                        onChange={(e) => { params.api.setEditCellValue(e.target.value); }}
                        select
                        fullWidth
                    >
                        {world_countries.map((country) => (
                            <MenuItem key={country.code} value={country.label}>
                                <Flag code={country.code} style={{ width: 20, height: 15, marginRight: 10 }} />
                                {country.label}
                            </MenuItem>
                        ))}
                    </TextField>
                );
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
            />
        </Box>
    );

};

export default Information;
