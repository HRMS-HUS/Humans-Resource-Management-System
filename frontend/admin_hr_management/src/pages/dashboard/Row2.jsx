import { DownloadOutlined } from "@mui/icons-material"
import { Box, IconButton, Paper, Stack, Typography, useTheme } from "@mui/material"
import { useNavigate } from "react-router-dom"
import Line from "../../pages/lineChart/Line"

const Row2 = () => {

    const theme = useTheme()
    const navigate = useNavigate()

    return (
        <Stack direction={'row'} flexWrap={'wrap'} gap={1.5} mt={3} sx={{ width: '100%', height: '100%' }}>
            <Paper onClick={() => { navigate('line') }} sx={{ width: '100%', height: '100%', maxWidth: 'none', cursor: "pointer", }}>
                <Stack alignItems={'center'} direction={'row'} flexWrap={'wrap'} justifyContent={"space-between"} sx={{ width: '100%', height: '100%', padding: 2, }}>
                    <Box sx={{ width: '100%' }}>
                        <Typography color={theme.palette.secondary.main} mt={2} ml={4} variant="h6">
                            Departmental Allowance and Deduction Report
                        </Typography>
                    </Box>
                </Stack>
                <Line isDashboard={true} />
            </Paper>
        </Stack>

    )
}

export default Row2
