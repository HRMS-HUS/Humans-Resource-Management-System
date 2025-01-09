import { Autocomplete, Box, IconButton, InputBase, Modal, Stack, styled, TextField, Toolbar, useTheme } from '@mui/material'
import { alpha } from '@mui/material/styles';
import MenuIcon from '@mui/icons-material/Menu';
import MuiAppBar from '@mui/material/AppBar';
import Person2OutlinedIcon from '@mui/icons-material/Person2Outlined';
import SettingsOutlinedIcon from '@mui/icons-material/SettingsOutlined';
import NotificationsNoneOutlinedIcon from '@mui/icons-material/NotificationsNoneOutlined';
import LightModeOutlinedIcon from '@mui/icons-material/LightModeOutlined';
import DarkModeOutlinedIcon from '@mui/icons-material/DarkModeOutlined';
import { useState } from 'react';
import Notification from '../pages/notification/Notification';
import { useNavigate } from 'react-router-dom';
import { Array1, Array2, Array3 } from './Sidebar';

const drawerWidth = 260;

const AppBar = styled(MuiAppBar, {
    shouldForwardProp: (prop) => prop !== 'open',
})(({ theme }) => ({
    zIndex: theme.zIndex.drawer + 1,
    transition: theme.transitions.create(['width', 'margin'], {
        easing: theme.transitions.easing.sharp,
        duration: theme.transitions.duration.leavingScreen,
    }),
    variants: [
        {
            // @ts-ignore
            props: ({ open }) => open,
            style: {
                marginLeft: drawerWidth,
                width: `calc(100% - ${drawerWidth}px)`,
                transition: theme.transitions.create(['width', 'margin'], {
                    easing: theme.transitions.easing.sharp,
                    duration: theme.transitions.duration.enteringScreen,
                }),
            },
        },
    ],
}));

const Search = styled('div')(({ theme }) => ({
    position: 'relative',
    borderRadius: theme.shape.borderRadius,
    backgroundColor: alpha(theme.palette.common.white, 0.15),
    '&:hover': {
        backgroundColor: alpha(theme.palette.common.white, 0.25),
    },
    marginRight: theme.spacing(2),
    marginLeft: 0,
    width: '100%',
    [theme.breakpoints.up('sm')]: {
        marginLeft: theme.spacing(3),
        width: '350px',
    },
}));

const menuItems = Array1.concat(Array2, Array3).map(item => ({
    text: item.text,
    path: item.path
}))

const TopBar = ({ open, handleDrawerOpen, setMode }) => {

    const theme = useTheme()
    const navigate = useNavigate()
    const [notification, setNotification] = useState(false)
    const handleOpen = () => setNotification(true);
    const handleClose = () => setNotification(false);

    const handleSearchChange = (event, newValue) => {
        if (newValue) {
            const selectedItem = menuItems.find((item) => item.text === newValue);
            if (selectedItem) {
                navigate(`${selectedItem.path}`)
            }
        }
    };

    return (
        <AppBar position="fixed"
            // @ts-ignore
            open={open}>
            <Toolbar>

                <IconButton
                    color="inherit"
                    aria-label="open drawer"
                    onClick={handleDrawerOpen}
                    edge="start"
                    sx={[
                        {
                            marginRight: 5,
                        },
                        open && { display: 'none' },
                    ]}
                >
                    <MenuIcon />
                </IconButton>

                <Search>
                    <Autocomplete
                        freeSolo
                        id="free-solo-2-demo"
                        options={menuItems.map((option) => option.text)}
                        onChange={handleSearchChange}
                        renderInput={(params) => (
                            <TextField
                                {...params}
                                placeholder='Search'
                                sx={{
                                    "& .MuiInputBase-root": { height: 45 },
                                    "& .MuiInputLabel-root": { top: -6 },
                                }}
                                slotProps={{
                                    input: {
                                        ...params.InputProps
                                    },
                                }}
                            />
                        )}
                    />
                </Search>

                <Box flexGrow={1} />

                <Stack direction={"row"}>

                    {theme.palette.mode === "light" ? (
                        <IconButton onClick={() => {
                            localStorage.setItem("currentMode", theme.palette.mode === 'dark' ? 'light' : 'dark')
                            setMode((prevMode) => prevMode === 'light' ? 'dark' : 'light')
                        }} color='inherit' >
                            <LightModeOutlinedIcon />
                        </IconButton>
                    ) : (
                        <IconButton onClick={() => {
                            localStorage.setItem("currentMode", theme.palette.mode === 'dark' ? 'light' : 'dark')
                            setMode((prevMode) => prevMode === 'light' ? 'dark' : 'light')
                        }} color='inherit'>
                            <DarkModeOutlinedIcon />
                        </IconButton>
                    )}

                    <IconButton color='inherit' onClick={handleOpen}>
                        <NotificationsNoneOutlinedIcon />
                    </IconButton>
                    <Modal
                        open={notification}
                        onClose={handleClose}
                        aria-labelledby="modal-modal-title"
                        aria-describedby="modal-modal-description"
                    >
                        <Notification />
                    </Modal>

                    <IconButton color='inherit'>
                        <SettingsOutlinedIcon />
                    </IconButton>

                    <IconButton color='inherit'>
                        <Person2OutlinedIcon />
                    </IconButton>

                </Stack>

            </Toolbar>
        </AppBar >
    )
}

export default TopBar