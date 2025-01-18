import { DownloadOutlined } from '@mui/icons-material'
import { Box } from '@mui/material'
import Button from '@mui/material/Button'
import Header from '../../components/Header'
import Row1 from './Row1'
import Row2 from './Row2'
import Row3 from './Row3'

const Dashboard = () => {
    return (
        <div>
            <Header isDashboard={true} title={"DASHBOARD"} subTitle={"Welcome to Dashboard"} />
            <Box sx={{ textAlign: "right", mb: 1.3 }}>
                <Button sx={{ padding: "6px 8px", textTransform: "capitalize" }} variant='contained' color='primary'>
                    <DownloadOutlined />
                    Download Reports
                </Button>
            </Box>
            <Row1 />
            <Row2 />
            <Row3 />
        </div>
    )
}

export default Dashboard
