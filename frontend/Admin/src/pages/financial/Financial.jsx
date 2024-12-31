import { Box, Button, LinearProgress, Rating, useTheme } from '@mui/material';
import { DataGrid, getGridNumericOperators, GridActionsCellItem, GridRowEditStopReasons, GridRowModes, GridToolbar, GridToolbarContainer } from '@mui/x-data-grid';
import { randomId } from '@mui/x-data-grid-generator';
import AddCardIcon from '@mui/icons-material/AddCard';
import { useImperativeHandle, useRef, useState } from 'react';
import { bankLogos, initialRows } from './data';
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/DeleteOutlined';
import SaveIcon from '@mui/icons-material/Save';
import CancelIcon from '@mui/icons-material/Close';
import Header from '../../components/Header';

function RatingInputValue(props) {
    const { item, applyValue, focusElementRef } = props;

    const ratingRef = useRef(null);
    useImperativeHandle(focusElementRef, () => ({
        focus: () => {
            ratingRef.current
                .querySelector(`input[value="${Number(item.value) || ''}"]`)
                .focus();
        },
    }));

    const handleFilterChange = (event, newValue) => {
        applyValue({ ...item, value: newValue });
    };

    return (
        <Box sx={{ display: 'inline-flex', flexDirection: 'row', alignItems: 'center', height: 48, pl: '20px' }}>
            <Rating
                name="custom-rating-filter-operator"
                value={Number(item.value)}
                onChange={handleFilterChange}
                precision={0.5}
                ref={ratingRef}
            />
        </Box>
    );
}

const salaryNetOperators = [
    {
        label: 'Above',
        value: 'above',
        getApplyFilterFn: (filterItem) => {
            if (!filterItem.field || !filterItem.value || !filterItem.operator) {
                return null;
            }
            return (value) => Math.floor((Number(value) - Math.min(...initialRows.map(item => item.salaryNet))) / (Math.max(...initialRows.map(item => item.salaryNet)) - Math.min(...initialRows.map(item => item.salaryNet))) * 10) / 2 >= Number(filterItem.value);
        },
        InputComponent: RatingInputValue,
        InputComponentProps: { type: 'number' },
        getValueAsString: (value) => `${value} Stars`,
    },
];

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
            <Button color="primary" startIcon={<AddCardIcon />} onClick={handleClick}>
                Add Record
            </Button>
        </GridToolbarContainer>
    );
}

const Financial = () => {

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
        { field: "name", headerName: "Full Name", cellClassName: "name-column--cell", width: 180, editable: true },
        { field: "salaryBasic", headerName: "Basic Salary", width: 180, align: "center", headerAlign: "center", editable: true, type: 'number' },
        { field: "salaryGross", headerName: "Gross Salary", width: 180, align: "center", headerAlign: "center", editable: true, type: 'number' },
        {
            field: "salaryNet", headerName: "Net Salary", width: 210, align: "left", headerAlign: "center", editable: true, type: 'number',
            filterOperators: [
                ...getGridNumericOperators(),
                ...salaryNetOperators
            ],
            renderCell: (params) => (
                <Box sx={{ display: 'flex', alignItems: 'center' }}>
                    {params.value.toFixed(2)}
                    <Rating value={Math.floor((params.value - Math.min(...initialRows.map(item => item.salaryNet))) / (Math.max(...initialRows.map(item => item.salaryNet)) - Math.min(...initialRows.map(item => item.salaryNet))) * 10) / 2} readOnly precision={0.5} style={{ marginLeft: 10 }} />
                </Box>
            )
        },
        {
            field: "allowanceHouseRent", headerName: "House Rent Allowance", width: 180, align: "center", headerAlign: "center", editable: true, type: 'number',
            renderCell: (params) => {
                const netSalary = params.row.salaryNet;
                const houseRentAllowance = params.value;
                const percentage = netSalary ? (houseRentAllowance / netSalary) * 100 : 0;

                return (
                    <Box sx={{ display: 'flex', alignItems: 'center', width: '100%' }}>
                        <LinearProgress
                            variant="determinate"
                            value={percentage}
                            sx={{
                                height: 22,
                                width: 90,
                                border: '0.25px',
                                backgroundColor: theme.palette.background.default,
                                borderColor: theme.palette.secondary.main,
                                '& .MuiLinearProgress-bar': {
                                    backgroundColor: "red",
                                }
                            }}
                        />
                        {percentage.toFixed(2)}%
                    </Box>
                );
            }
        },
        { field: "allowanceMedical", headerName: "Medical Allowance", width: 180, align: "center", headerAlign: "center", editable: true, type: 'number' },
        { field: "allowanceSpecial", headerName: "Special Allowance", width: 180, align: "center", headerAlign: "center", editable: true, type: 'number' },
        { field: "allowanceFuel", headerName: "Fuel Allowance", width: 180, align: "center", headerAlign: "center", editable: true, type: 'number' },
        { field: "allowancePhoneBill", headerName: "Phone Bill Allowance", width: 180, align: "center", headerAlign: "center", editable: true, type: 'number' },
        { field: "allowanceOther", headerName: "Other Allowance", width: 180, align: "center", headerAlign: "center", editable: true, type: 'number' },
        { field: "allowanceTotal", headerName: "Total Allowance", width: 180, align: "center", headerAlign: "center", editable: true, type: 'number' },
        { field: "deductionProvidentFund", headerName: "Provident Fund Deduction", width: 180, align: "center", headerAlign: "center", editable: true, type: 'number' },
        { field: "deductionTax", headerName: "Tax Deduction", width: 180, align: "center", headerAlign: "center", editable: true, type: 'number' },
        { field: "deductionOther", headerName: "Other Deductions", width: 180, align: "center", headerAlign: "center", editable: true, type: 'number' },
        { field: "deductionTotal", headerName: "Total Deductions", width: 180, align: "center", headerAlign: "center", editable: true, type: 'number' },
        {
            field: "bankName", headerName: "Bank Name", width: 150, align: "left", headerAlign: "left", editable: true,
            renderCell: ({ row: { bankName } }) => {
                const bank = bankLogos.find(item => item.name === bankName)
                if (!bank) { return null }
                return (
                    <Box sx={{ display: 'flex', alignItems: 'center' }}>
                        <img src={bank.URL} style={{ width: 20, height: 20, marginRight: 10 }} />
                        {bankName}
                    </Box>
                );
            }
        },
        {
            field: "accountName", headerName: "Account Name", width: 150, align: "left", headerAlign: "left", editable: true,
            renderCell: (params) => {
                return <div style={{ textTransform: 'uppercase' }}>{params.value}</div>;
            }
        },
        { field: "accountNumber", headerName: "Account Number", width: 150, align: "center", headerAlign: "center", editable: true },
        { field: "iban", headerName: "IBAN", width: 150, align: "center", headerAlign: "center", editable: true },
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
    ]

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
    )
}

export default Financial
