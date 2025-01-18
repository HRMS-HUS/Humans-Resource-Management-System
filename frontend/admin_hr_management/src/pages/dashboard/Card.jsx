import { Box, Paper, Stack, Typography, useTheme } from '@mui/material'

const Card = ({ icon, title, subTitle }) => {

    const theme = useTheme()

    return (
        <Paper sx={{ flexGrow: 1, minWidth: "290px", height: "140px", p: 1.5, display: "flex", justifyContent: "space-between" }}>
            <Stack gap={2}>
                <Typography variant='body2' sx={{ fontSize: "20px", color: theme.palette.info.light, }}>{title}</Typography>
                <Typography variant='body2' sx={{ fontSize: "20px" }}>{subTitle}</Typography>
            </Stack>
            <Box height={'70px'} width={'70px'}>
                {icon}
            </Box>
        </Paper>
    )
}

export default Card
