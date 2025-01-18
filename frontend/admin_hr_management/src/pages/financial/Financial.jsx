import { Alert, Box, Button, LinearProgress, Rating, Snackbar, useTheme } from '@mui/material';
import { DataGrid, getGridNumericOperators, GridActionsCellItem, GridRowEditStopReasons, GridRowModes, GridToolbar, GridToolbarContainer } from '@mui/x-data-grid';
import { randomId } from '@mui/x-data-grid-generator';
import AddCardIcon from '@mui/icons-material/AddCard';
import { useEffect, useImperativeHandle, useRef, useState } from 'react';
import { bankLogos } from './data';
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/DeleteOutlined';
import SaveIcon from '@mui/icons-material/Save';
import CancelIcon from '@mui/icons-material/Close';
import Header from '../../components/Header';
import axios from 'axios';
import { useAuthStore } from '../login/authStore';

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

function EditToolbar(props) {
    const { setRows, setRowModesModel } = props;

    const handleClick = () => {
        const id = randomId();
        setRows((oldRows) => [
            ...oldRows,
            { id, user_id: '', name: '', salaryBasic: '', salaryGross: '', salaryNet: '', allowanceHouseRent: '', allowanceMedical: '', allowanceSpecial: '', allowanceFuel: '', allowancePhoneBill: '', allowanceOther: '', allowanceTotal: '', deductionProvidentFund: '', deductionTax: '', deductionOther: '', deductionTotal: '', bankName: '', accountName: '', accountNumber: '', isNew: true }
        ]);
        setRowModesModel((oldModel) => ({
            ...oldModel,
            [id]: { mode: GridRowModes.Edit, fieldToFocus: 'user_id' },
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
    const [rows, setRows] = useState([]);
    const [rowModesModel, setRowModesModel] = useState({});
    const [loading, setLoading] = useState(null);
    const [snackbar, setSnackbar] = useState({ open: false, message: '', severity: 'success' });
    const { token } = useAuthStore()

    const fetchFinancialInformation = async () => {
        setLoading(true);
        try {
            const [financialInfoResponse, userInfoResponse] = await Promise.all([
                axios.get('http://52.184.86.56:8000/api/admin/financial_info', {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                }),
                axios.get('http://52.184.86.56:8000/api/admin/personal_info', {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                })
            ]);

            const dataWithId = await Promise.all(financialInfoResponse.data.map(async (item) => {
                const user_name = userInfoResponse.data.find(user => user.user_id === item.user_id)?.fullname || "Unknown User";
                return {
                    ...item,
                    id: item.financial_info_id,
                    name: user_name
                };
            }));

            setRows(dataWithId);
        } catch (error) {
            console.error("Error fetching financial information:", error);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchFinancialInformation();
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
        fetchFinancialInformation();
    };

    const handleDeleteClick = (id) => async () => {
        const financial_info_delete = rows.find((row) => row.id === id);
        const financial_info_id = financial_info_delete.financial_info_id;

        try {
            const response = await axios.delete(`http://52.184.86.56:8000/api/financial_info/${financial_info_id}`, {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            });
            if (response.status === 200) {
                setRows(rows.filter((row) => row.id !== id));
                setSnackbar({ open: true, message: 'Financial information deleted successfully!', severity: 'success' });
                fetchFinancialInformation();
            } else {
                console.error('Error deleting financial information:', response.data);
                setSnackbar({ open: true, message: 'Failed to delete financial information!', severity: 'error' });
            }
        } catch (error) {
            console.error('Error deleting financial information:', error);
            setSnackbar({ open: true, message: 'Failed to delete financial information!', severity: 'error' });
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

    const handleSnackbarClose = () => setSnackbar({ ...snackbar, open: false });

    const processRowUpdate = async (newRow) => {
        const updatedRow = { ...newRow, isNew: false };

        const allowanceTotal = newRow.allowanceHouseRent + newRow.allowanceMedical + newRow.allowanceSpecial +
            newRow.allowanceFuel + newRow.allowancePhoneBill + newRow.allowanceOther;
        const deductionTotal = newRow.deductionProvidentFund + newRow.deductionTax + newRow.deductionOther;
        const salaryNet = newRow.salaryGross + allowanceTotal - deductionTotal;

        updatedRow.allowanceTotal = allowanceTotal;
        updatedRow.deductionTotal = deductionTotal;
        updatedRow.salaryNet = salaryNet;

        try {
            if (newRow.isNew) {
                const response = await axios.post('http://52.184.86.56:8000/api/admin/financial_info', null, {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    },
                    params: {
                        user_id: newRow.user_id,
                        salaryBasic: newRow.salaryBasic,
                        salaryGross: newRow.salaryGross,
                        salaryNet: salaryNet,
                        allowanceHouseRent: newRow.allowanceHouseRent,
                        allowanceMedical: newRow.allowanceMedical,
                        allowanceSpecial: newRow.allowanceSpecial,
                        allowanceFuel: newRow.allowanceFuel,
                        allowancePhoneBill: newRow.allowancePhoneBill,
                        allowanceOther: newRow.allowanceOther,
                        allowanceTotal: allowanceTotal,
                        deductionProvidentFund: newRow.deductionProvidentFund,
                        deductionTax: newRow.deductionTax,
                        deductionOther: newRow.deductionOther,
                        deductionTotal: deductionTotal,
                        bankName: newRow.bankName,
                        accountName: newRow.accountName,
                        accountNumber: newRow.accountNumber,
                        iban: newRow.iban
                    }
                });

                updatedRow.user_id = response.data.user_id;
                setRows(prevRows => [...prevRows.filter(row => row.id !== updatedRow.id), updatedRow]);
                setSnackbar({ open: true, message: 'Financial information created successfully!', severity: 'success' });
                fetchFinancialInformation();
                return updatedRow;
            } else {
                const response = await axios.put(`http://52.184.86.56:8000/api/admin/financial_info/${newRow.financial_info_id}`, null, {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    },
                    params: {
                        user_id: newRow.user_id,
                        salaryBasic: newRow.salaryBasic,
                        salaryGross: newRow.salaryGross,
                        salaryNet: salaryNet,
                        allowanceHouseRent: newRow.allowanceHouseRent,
                        allowanceMedical: newRow.allowanceMedical,
                        allowanceSpecial: newRow.allowanceSpecial,
                        allowanceFuel: newRow.allowanceFuel,
                        allowancePhoneBill: newRow.allowancePhoneBill,
                        allowanceOther: newRow.allowanceOther,
                        allowanceTotal: allowanceTotal,
                        deductionProvidentFund: newRow.deductionProvidentFund,
                        deductionTax: newRow.deductionTax,
                        deductionOther: newRow.deductionOther,
                        deductionTotal: deductionTotal,
                        bankName: newRow.bankName,
                        accountName: newRow.accountName,
                        accountNumber: newRow.accountNumber,
                        iban: newRow.iban
                    }
                });

                setSnackbar({ open: true, message: 'Financial information updated successfully!', severity: 'success' });
                fetchFinancialInformation();
                return updatedRow;
            }
        } catch (error) {
            console.error('Error saving data:', error.response?.data || error.message);
            setSnackbar({ open: true, message: 'Failed to save financial information!', severity: 'error' });
            throw error;
        }
    };


    const handleRowModesModelChange = (newRowModesModel) => {
        setRowModesModel(newRowModesModel);
    };

    const salaryNetOperators = [
        {
            label: 'Above',
            value: 'above',
            getApplyFilterFn: (filterItem) => {
                if (!filterItem.field || !filterItem.value || !filterItem.operator) {
                    return null;
                }
                return (value) => Math.floor((Number(value) - Math.min(...rows.map(item => item.salaryNet))) / (Math.max(...rows.map(item => item.salaryNet)) - Math.min(...rows.map(item => item.salaryNet))) * 10) / 2 >= Number(filterItem.value);
            },
            InputComponent: RatingInputValue,
            InputComponentProps: { type: 'number' },
            getValueAsString: (value) => `${value} Stars`,
        },
    ];

    const columns = [
        { field: "user_id", headerName: "User ID", width: 80, align: "center", headerAlign: "center", editable: true },
        { field: "name", headerName: "Full Name", cellClassName: "name-column--cell", width: 180, editable: false },
        {
            field: "salaryBasic", headerName: "Basic Salary", width: 180, align: "center", headerAlign: "center", editable: true, type: 'number',
            renderCell: (params) => {
                return `${params.value.toLocaleString()}`;
            }
        },
        {
            field: "salaryGross", headerName: "Gross Salary", width: 180, align: "center", headerAlign: "center", editable: true, type: 'number',
            renderCell: (params) => {
                return `${params.value.toLocaleString()}`;
            }
        },
        {
            field: "salaryNet", headerName: "Net Salary", width: 210, align: "left", headerAlign: "center", editable: true, type: 'number',
            filterOperators: [
                ...getGridNumericOperators(),
                ...salaryNetOperators
            ],
            renderCell: (params) => (
                <Box sx={{ display: 'flex', alignItems: 'center' }}>
                    <Rating value={Math.floor((params.value - Math.min(...rows.map(item => item.salaryNet))) / (Math.max(...rows.map(item => item.salaryNet)) - Math.min(...rows.map(item => item.salaryNet))) * 10) / 2} readOnly precision={0.5} style={{ marginRight: 10 }} />
                    {params.value.toLocaleString()}
                </Box>
            )
        },
        {
            field: "allowanceHouseRent", headerName: "House Rent Allowance", width: 190, align: "center", headerAlign: "center", editable: true, type: 'number',
            renderCell: (params) => {
                const percentage = params.row.salaryGross ? (params.value / params.row.salaryGross) * 100 : 0;
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
                                        backgroundColor: percentage < 5
                                            ? "#e74c3c"
                                            : percentage >= 5 && percentage < 10
                                                ? "#33CCCC"
                                                : percentage >= 10 && percentage < 15
                                                    ? "#00CC33"
                                                    : "#607d8b",
                                    }
                                }}
                            />
                            <Box sx={{ position: 'absolute', top: '50%', left: '50%', transform: 'translate(-50%, -50%)', color: theme.palette.text.primary, fontSize: '0.9rem' }}>
                                {percentage.toFixed(2)}%
                            </Box>
                        </Box>
                        {params.value.toLocaleString()}
                    </div>
                );
            }
        },
        {
            field: "allowanceMedical", headerName: "Medical Allowance", width: 190, align: "center", headerAlign: "center", editable: true, type: 'number',
            renderCell: (params) => {
                const percentage = params.row.salaryGross ? (params.value / params.row.salaryGross) * 100 : 0;
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
                                        backgroundColor: percentage < 5
                                            ? "#e74c3c"
                                            : percentage >= 5 && percentage < 10
                                                ? "#33CCCC"
                                                : percentage >= 10 && percentage < 15
                                                    ? "#00CC33"
                                                    : "#607d8b",
                                    }
                                }}
                            />
                            <Box sx={{ position: 'absolute', top: '50%', left: '50%', transform: 'translate(-50%, -50%)', color: theme.palette.text.primary, fontSize: '0.9rem' }}>
                                {percentage.toFixed(2)}%
                            </Box>
                        </Box>
                        {params.value.toLocaleString()}
                    </div>
                );
            }
        },
        {
            field: "allowanceSpecial", headerName: "Special Allowance", width: 190, align: "center", headerAlign: "center", editable: true, type: 'number',
            renderCell: (params) => {
                const percentage = params.row.salaryGross ? (params.value / params.row.salaryGross) * 100 : 0;
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
                                        backgroundColor: percentage < 5
                                            ? "#e74c3c"
                                            : percentage >= 5 && percentage < 10
                                                ? "#33CCCC"
                                                : percentage >= 10 && percentage < 15
                                                    ? "#00CC33"
                                                    : "#607d8b",
                                    }
                                }}
                            />
                            <Box sx={{ position: 'absolute', top: '50%', left: '50%', transform: 'translate(-50%, -50%)', color: theme.palette.text.primary, fontSize: '0.9rem' }}>
                                {percentage.toFixed(2)}%
                            </Box>
                        </Box>
                        {params.value.toLocaleString()}
                    </div>
                );
            }
        },
        {
            field: "allowanceFuel", headerName: "Fuel Allowance", width: 190, align: "center", headerAlign: "center", editable: true, type: 'number',
            renderCell: (params) => {
                const percentage = params.row.salaryGross ? (params.value / params.row.salaryGross) * 100 : 0;
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
                                        backgroundColor: percentage < 5
                                            ? "#e74c3c"
                                            : percentage >= 5 && percentage < 10
                                                ? "#33CCCC"
                                                : percentage >= 10 && percentage < 15
                                                    ? "#00CC33"
                                                    : "#607d8b",
                                    }
                                }}
                            />
                            <Box sx={{ position: 'absolute', top: '50%', left: '50%', transform: 'translate(-50%, -50%)', color: theme.palette.text.primary, fontSize: '0.9rem' }}>
                                {percentage.toFixed(2)}%
                            </Box>
                        </Box>
                        {params.value.toLocaleString()}
                    </div>
                );
            }
        },
        {
            field: "allowancePhoneBill", headerName: "Phone Bill Allowance", width: 190, align: "center", headerAlign: "center", editable: true, type: 'number',
            renderCell: (params) => {
                const percentage = params.row.salaryGross ? (params.value / params.row.salaryGross) * 100 : 0;
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
                                        backgroundColor: percentage < 5
                                            ? "#e74c3c"
                                            : percentage >= 5 && percentage < 10
                                                ? "#33CCCC"
                                                : percentage >= 10 && percentage < 15
                                                    ? "#00CC33"
                                                    : "#607d8b",
                                    }
                                }}
                            />
                            <Box sx={{ position: 'absolute', top: '50%', left: '50%', transform: 'translate(-50%, -50%)', color: theme.palette.text.primary, fontSize: '0.9rem' }}>
                                {percentage.toFixed(2)}%
                            </Box>
                        </Box>
                        {params.value.toLocaleString()}
                    </div>
                );
            }
        },
        {
            field: "allowanceOther", headerName: "Other Allowance", width: 190, align: "center", headerAlign: "center", editable: true, type: 'number',
            renderCell: (params) => {
                const percentage = params.row.salaryGross ? (params.value / params.row.salaryGross) * 100 : 0;
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
                                        backgroundColor: percentage < 5
                                            ? "#e74c3c"
                                            : percentage >= 5 && percentage < 10
                                                ? "#33CCCC"
                                                : percentage >= 10 && percentage < 15
                                                    ? "#00CC33"
                                                    : "#607d8b",
                                    }
                                }}
                            />
                            <Box sx={{ position: 'absolute', top: '50%', left: '50%', transform: 'translate(-50%, -50%)', color: theme.palette.text.primary, fontSize: '0.9rem' }}>
                                {percentage.toFixed(2)}%
                            </Box>
                        </Box>
                        {params.value.toLocaleString()}
                    </div>
                );
            }
        },
        {
            field: "allowanceTotal", headerName: "Total Allowance", width: 190, align: "center", headerAlign: "center", editable: true, type: 'number',
            renderCell: (params) => {
                const percentage = params.row.salaryGross ? (params.value / params.row.salaryGross) * 100 : 0;
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
                                        backgroundColor: percentage < 5
                                            ? "#e74c3c"
                                            : percentage >= 5 && percentage < 10
                                                ? "#33CCCC"
                                                : percentage >= 10 && percentage < 15
                                                    ? "#00CC33"
                                                    : "#607d8b",
                                    }
                                }}
                            />
                            <Box sx={{ position: 'absolute', top: '50%', left: '50%', transform: 'translate(-50%, -50%)', color: theme.palette.text.primary, fontSize: '0.9rem' }}>
                                {percentage.toFixed(2)}%
                            </Box>
                        </Box>
                        {params.value.toLocaleString()}
                    </div>
                );
            }
        },
        {
            field: "deductionProvidentFund", headerName: "Provident Fund Deduction", width: 190, align: "center", headerAlign: "center", editable: true, type: 'number',
            renderCell: (params) => {
                const percentage = params.row.salaryGross ? (params.value / params.row.salaryGross) * 100 : 0;
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
                                        backgroundColor: percentage < 5
                                            ? "#e74c3c"
                                            : percentage >= 5 && percentage < 10
                                                ? "#33CCCC"
                                                : percentage >= 10 && percentage < 15
                                                    ? "#00CC33"
                                                    : "#607d8b",
                                    }
                                }}
                            />
                            <Box sx={{ position: 'absolute', top: '50%', left: '50%', transform: 'translate(-50%, -50%)', color: theme.palette.text.primary, fontSize: '0.9rem' }}>
                                {percentage.toFixed(2)}%
                            </Box>
                        </Box>
                        {params.value.toLocaleString()}
                    </div>
                );
            }
        },
        {
            field: "deductionTax", headerName: "Tax Deduction", width: 190, align: "center", headerAlign: "center", editable: true, type: 'number',
            renderCell: (params) => {
                const percentage = params.row.salaryGross ? (params.value / params.row.salaryGross) * 100 : 0;
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
                                        backgroundColor: percentage < 5
                                            ? "#e74c3c"
                                            : percentage >= 5 && percentage < 10
                                                ? "#33CCCC"
                                                : percentage >= 10 && percentage < 15
                                                    ? "#00CC33"
                                                    : "#607d8b",
                                    }
                                }}
                            />
                            <Box sx={{ position: 'absolute', top: '50%', left: '50%', transform: 'translate(-50%, -50%)', color: theme.palette.text.primary, fontSize: '0.9rem' }}>
                                {percentage.toFixed(2)}%
                            </Box>
                        </Box>
                        {params.value.toLocaleString()}
                    </div>
                );
            }
        },
        {
            field: "deductionOther", headerName: "Other Deductions", width: 190, align: "center", headerAlign: "center", editable: true, type: 'number',
            renderCell: (params) => {
                const percentage = params.row.salaryGross ? (params.value / params.row.salaryGross) * 100 : 0;
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
                                        backgroundColor: percentage < 5
                                            ? "#e74c3c"
                                            : percentage >= 5 && percentage < 10
                                                ? "#33CCCC"
                                                : percentage >= 10 && percentage < 15
                                                    ? "#00CC33"
                                                    : "#607d8b",
                                    }
                                }}
                            />
                            <Box sx={{ position: 'absolute', top: '50%', left: '50%', transform: 'translate(-50%, -50%)', color: theme.palette.text.primary, fontSize: '0.9rem' }}>
                                {percentage.toFixed(2)}%
                            </Box>
                        </Box>
                        {params.value.toLocaleString()}
                    </div>
                );
            }
        },
        {
            field: "deductionTotal", headerName: "Total Deductions", width: 190, align: "center", headerAlign: "center", editable: true, type: 'number',
            renderCell: (params) => {
                const percentage = params.row.salaryGross ? (params.value / params.row.salaryGross) * 100 : 0;
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
                                        backgroundColor: percentage < 5
                                            ? "#e74c3c"
                                            : percentage >= 5 && percentage < 10
                                                ? "#33CCCC"
                                                : percentage >= 10 && percentage < 15
                                                    ? "#00CC33"
                                                    : "#607d8b",
                                    }
                                }}
                            />
                            <Box sx={{ position: 'absolute', top: '50%', left: '50%', transform: 'translate(-50%, -50%)', color: theme.palette.text.primary, fontSize: '0.9rem' }}>
                                {percentage.toFixed(2)}%
                            </Box>
                        </Box>
                        {params.value.toLocaleString()}
                    </div>
                );
            }
        },
        {
            field: "bankName", headerName: "Bank Name", width: 150, align: "left", headerAlign: "left", editable: true, type: 'singleSelect', valueOptions: bankLogos.map(item => item.name),
            renderCell: ({ row: { bankName } }) => {
                const bank = bankLogos.find(item => item.name === bankName)
                if (!bank) { return null }
                return (
                    <Box sx={{ display: 'flex', alignItems: 'center' }}>
                        <img src={bank.URL} style={{ width: bank.width, height: bank.height, marginRight: bank.marginRight }} />
                        {bankName}
                    </Box>
                );
            }
        },
        {
            field: "accountName", headerName: "Account Name", width: 150, align: "left", headerAlign: "left", editable: true,
            renderCell: (params) => {
                const removeVietnameseTones = (str) => { return str.normalize('NFD').replace(/[\u0300-\u036f]/g, ''); };
                return <div style={{ textTransform: 'uppercase' }}>{removeVietnameseTones(params.value)}</div>;
            }
        },
        { field: "accountNumber", headerName: "Account Number", width: 150, align: "center", headerAlign: "center", editable: true },
        { field: "iban", headerName: "IBAN", width: 150, align: "center", headerAlign: "center", editable: true },
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
    ]

    return (
        <Box sx={{ height: 600, width: '98%', mx: "auto" }}>
            <Header title={'Financial Information'} subTitle={'Manage all employees financial information'} />
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
    )
}

export default Financial
