import { Box, Paper, Stack, Typography, useTheme } from '@mui/material'
import Map from '../../pages/geography/Map'
import Bar from '../../pages/barChart/Bar'
import Pie from '../../pages/pieChart/Pie'
import { useNavigate } from "react-router-dom"

const Row3 = () => {

    const theme = useTheme()
    const navigate = useNavigate()

    return (
        <Stack gap={1.5} direction={"row"} flexWrap={"wrap"} mt={3}>

            <Paper onClick={() => { navigate('pie') }} sx={{ flexGrow: 1, minWidth: "300px", width: "28%", cursor: "pointer" }}>
                <Typography
                    color={theme.palette.secondary.main}
                    sx={{ padding: "30px 30px 0 30px", mb: '20px' }}
                    variant="h6"
                    fontWeight="600"
                >
                    Employees of Department
                </Typography>
                <Pie isDashboard={true} />
                <Typography variant="h6" align="center" sx={{ mt: "10px" }}>
                    Number of employees per department
                </Typography>
            </Paper>

            <Paper onClick={() => { navigate('bar') }} sx={{ flexGrow: 1, minWidth: "300px", width: "33%", cursor: "pointer" }}>
                <Typography
                    color={theme.palette.secondary.main}
                    sx={{ padding: "30px 30px 0 30px" }}
                    variant="h6"
                    fontWeight="600"
                >
                    Net Salary of Department
                </Typography>
                <Bar isDashboard={true} />
                <Typography variant="h6" align="center" sx={{ mb: '20px' }}>
                    Total Net Salary per department
                </Typography>
            </Paper>

            <Paper onClick={() => { navigate('geography') }} sx={{ flexGrow: 1, minWidth: "300px", width: "33%", cursor: "pointer" }}>
                <Map isDashboard={true} />
            </Paper>

        </Stack>
    )
}

export default Row3
