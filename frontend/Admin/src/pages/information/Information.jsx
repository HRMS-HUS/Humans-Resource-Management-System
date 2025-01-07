import { Box, Button, MenuItem, TextField, Typography, useTheme } from '@mui/material';
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

function EditToolbar(props) {
    const { setRows, setRowModesModel } = props;

    const handleClick = () => {
        const id = randomId();
        setRows((oldRows) => [
            ...oldRows,
            { id, user_id: '', fullname: '', citizen_card: '', department: '', date_of_birth: '', phone: '', email: '', marital_status: '', address: '', city: '', country: '', isNew: true }
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

    const fetchDepartmentInfo = async (departmentId) => {
        try {
            const response = await axios.get(`http://127.0.0.1:8000/api/departments/${departmentId}`);
            return response.data.department_name;
        } catch (error) {
            console.error("Error fetching department info:", error);
            return "Unknown Department";
        }
    };

    const fetchInformation = async () => {
        setLoading(true);
        try {
            const response = await axios.get('http://127.0.0.1:8000/api/personal_info');
            const dataWithId = await Promise.all(response.data.map(async (item) => {
                const departmentName = await fetchDepartmentInfo(item.department_id);
                return {
                    ...item,
                    id: item.user_id,
                    manager_name: departmentName
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
        { field: "user_id", headerName: "ID", width: 80, align: "center", headerAlign: "center", editable: true },
        { field: "fullname", headerName: "Full Name", cellClassName: "name-column--cell", width: 180, editable: true },
        { field: "citizen_card", headerName: "Citizen ID Number", width: 160, align: "center", headerAlign: "center", editable: true },
        {
            field: "department", headerName: "Department", width: 210, align: "center", headerAlign: "center", editable: true, type: 'singleSelect', valueOptions: ["Software Development", "Cybersecurity", "Hardware Development", "Data Development", "Research and Development", "Marketing", "Humans Resource", "Finance", "Design", "Legal", "Customer Support"].sort(),
            renderCell: ({ row: { department } }) => {
                return (
                    <Box sx={{ p: "2px", display: "flex", justifyContent: "left", alignItems: "center", height: "100%" }}>
                        {department === "Software Development" && (<ImportantDevicesIcon sx={{ marginRight: 1 }} fontSize='medium' />)}
                        {department === "Cybersecurity" && (<LockIcon sx={{ marginRight: 1 }} fontSize='medium' />)}
                        {department === "Hardware Development" && (<SettingsInputComponentIcon sx={{ marginRight: 1 }} fontSize='medium' />)}
                        {department === "Data Development" && (<CloudDownloadIcon sx={{ marginRight: 1 }} fontSize='medium' />)}
                        {department === "Research and Development" && (<PsychologyIcon sx={{ marginRight: 1 }} fontSize='medium' />)}
                        {department === "Marketing" && (<TrendingUpIcon sx={{ marginRight: 1 }} fontSize='medium' />)}
                        {department === "Humans Resource" && (<GroupsIcon sx={{ marginRight: 1 }} fontSize='medium' />)}
                        {department === "Finance" && (<MonetizationOnIcon sx={{ marginRight: 1 }} fontSize='medium' />)}
                        {department === "Design" && (<DesignServicesIcon sx={{ marginRight: 1 }} fontSize='medium' />)}
                        {department === "Legal" && (<GavelIcon sx={{ marginRight: 1 }} fontSize='medium' />)}
                        {department === "Customer Support" && (<SupportAgentIcon sx={{ marginRight: 1 }} fontSize='medium' />)}
                        {department}
                    </Box>
                )
            }
        },
        {
            field: "date_of_birth", headerName: "Date of Birth", type: "date", width: 140, align: "center", headerAlign: "center", editable: true,
            valueGetter: (params) => {
                return params.row && params.row.date_of_birth ? new Date(params.row.date_of_birth) : null;
            },
            renderCell: (params) => {
                const dateOfBirth = params.row && params.row.date_of_birth;
                return dateOfBirth ? dayjs(dateOfBirth).format('DD/MM/YYYY') : '';
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
            field: "country", headerName: "Country", width: 150, editable: true, type: 'singleSelect', valueOptions: world_countries.map(country => country.label).sort(),
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
                loading={loading}
            />
        </Box>
    );

};

export default Information;
