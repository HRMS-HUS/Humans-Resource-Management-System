import List from '@mui/material/List';
import Divider from '@mui/material/Divider';
import IconButton from '@mui/material/IconButton';
import ChevronLeftIcon from '@mui/icons-material/ChevronLeft';
import ChevronRightIcon from '@mui/icons-material/ChevronRight';
import ListItem from '@mui/material/ListItem';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import HomeOutlinedIcon from '@mui/icons-material/HomeOutlined';
import ManageAccountsIcon from '@mui/icons-material/ManageAccounts';
import ContactsOutlinedIcon from '@mui/icons-material/ContactsOutlined';
import LocalAtmIcon from '@mui/icons-material/LocalAtm';
import PersonOutlinedIcon from '@mui/icons-material/PersonOutlined';
import CalendarTodayOutlinedIcon from '@mui/icons-material/CalendarTodayOutlined';
import HelpOutlineOutlinedIcon from '@mui/icons-material/HelpOutlineOutlined';
import BarChartOutlinedIcon from '@mui/icons-material/BarChartOutlined';
import PieChartOutlineOutlinedIcon from '@mui/icons-material/PieChartOutlineOutlined';
import TimelineOutlinedIcon from '@mui/icons-material/TimelineOutlined';
import MapOutlinedIcon from '@mui/icons-material/MapOutlined';
import ApartmentIcon from '@mui/icons-material/Apartment';
import { Avatar, styled, Tooltip, Typography, useTheme } from '@mui/material';
import MuiDrawer from '@mui/material/Drawer';
import { useLocation, useNavigate } from 'react-router-dom';
import { grey } from '@mui/material/colors'

const drawerWidth = 260;

const openedMixin = (theme) => ({
    width: drawerWidth,
    transition: theme.transitions.create('width', {
        easing: theme.transitions.easing.sharp,
        duration: theme.transitions.duration.enteringScreen,
    }),
    overflowX: 'hidden',
});

const closedMixin = (theme) => ({
    transition: theme.transitions.create('width', {
        easing: theme.transitions.easing.sharp,
        duration: theme.transitions.duration.leavingScreen,
    }),
    overflowX: 'hidden',
    width: `calc(${theme.spacing(7)} + 1px)`,
    [theme.breakpoints.up('sm')]: {
        width: `calc(${theme.spacing(8)} + 1px)`,
    },
});

const Drawer = styled(MuiDrawer, { shouldForwardProp: (prop) => prop !== 'open' })(
    ({ theme }) => ({
        width: drawerWidth,
        flexShrink: 0,
        whiteSpace: 'nowrap',
        boxSizing: 'border-box',
        variants: [
            {
                props: ({ open }) => open,
                style: {
                    ...openedMixin(theme),
                    '& .MuiDrawer-paper': openedMixin(theme),
                },
            },
            {
                props: ({ open }) => !open,
                style: {
                    ...closedMixin(theme),
                    '& .MuiDrawer-paper': closedMixin(theme),
                },
            },
        ],
    }),
);

const DrawerHeader = styled('div')(({ theme }) => ({
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'flex-end',
    padding: theme.spacing(0, 1),
    ...theme.mixins.toolbar,
}));

export const Array1 = [
    {
        text: "Dashboard",
        icon: <HomeOutlinedIcon />,
        path: "/",
    },
    {
        text: "Manage Account",
        icon: <ManageAccountsIcon />,
        path: "/account",
    },
    {
        text: "Employees Information",
        icon: <ContactsOutlinedIcon />,
        path: "/information",
    },
    {
        text: "Financial Information",
        icon: <LocalAtmIcon />,
        path: "/financial",
    },
    {
        text: "Departments",
        icon: <ApartmentIcon/>,
        path: "/department"
    }
];

export const Array2 = [
    {
        text: "Profile Form",
        icon: <PersonOutlinedIcon />,
        path: "/form",
    },
    {
        text: "Calendar",
        icon: <CalendarTodayOutlinedIcon />,
        path: "/calendar",
    },
    {
        text: "FAQ Page",
        icon: <HelpOutlineOutlinedIcon />,
        path: "/faq",
    },
];

export const Array3 = [
    {
        text: "Bar Chart",
        icon: <BarChartOutlinedIcon />,
        path: "/bar",
    },
    {
        text: "Pie Chart",
        icon: <PieChartOutlineOutlinedIcon />,
        path: "/pie",
    },
    {
        text: "Line Chart",
        icon: <TimelineOutlinedIcon />,
        path: "/line",
    },
    {
        text: "Geography Chart",
        icon: <MapOutlinedIcon />,
        path: "/geography",
    },
];

const Sidebar = ({ open, handleDrawerClose }) => {

    const theme = useTheme()
    const navigate = useNavigate()
    let location = useLocation()

    return (
        <Drawer variant="permanent" open={open}>
            <DrawerHeader>
                <IconButton onClick={handleDrawerClose}>
                    {theme.direction === 'rtl' ? <ChevronRightIcon /> : <ChevronLeftIcon />}
                </IconButton>
            </DrawerHeader>

            <Divider />

            <Avatar sx={{ mx: 'auto', width: open ? 100 : 44, height: open ? 100 : 44, my: 1, border: "2px solid grey", transition: '0.25s' }} alt="Remy Sharp" src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRLkCvaceexOvp91gxagcGAhWCc3yYCy4tGHw&s" />
            <Typography align='center' sx={{ fontSize: open ? 25 : 0, transition: '0.25s' }}>NVIDIA</Typography>
            <Typography align='center' sx={{ fontSize: open ? 18 : 0, transition: '0.25s', color: theme.palette.info.main }}>Administrator</Typography >

            <Divider />

            <List>
                {Array1.map((item) => (
                    <ListItem key={item.path} disablePadding sx={{ display: 'block' }}>

                        <Tooltip title={open ? null : item.text} placement="left">
                            <ListItemButton
                                onClick={() => { navigate(item.path) }}
                                sx={[
                                    {
                                        minHeight: 48,
                                        px: 2.5,
                                        bgcolor: location.pathname === item.path ? theme.palette.mode === 'dark' ? grey[800] : grey[300] : null
                                    },
                                    open
                                        ? {
                                            justifyContent: 'initial',
                                        }
                                        : {
                                            justifyContent: 'center',
                                        },
                                ]}
                            >
                                <ListItemIcon
                                    sx={[
                                        {
                                            minWidth: 0,
                                            justifyContent: 'center',
                                        },
                                        open
                                            ? {
                                                mr: 3,
                                            }
                                            : {
                                                mr: 'auto',
                                            },
                                    ]}
                                >
                                    {item.icon}
                                </ListItemIcon>
                                <ListItemText
                                    primary={item.text}
                                    sx={[
                                        open
                                            ? {
                                                opacity: 1,
                                            }
                                            : {
                                                opacity: 0,
                                            },
                                    ]}
                                />
                            </ListItemButton>
                        </Tooltip>

                    </ListItem>
                ))}
            </List>

            <Divider />

            <List>
                {Array2.map((item) => (
                    <ListItem key={item.path} disablePadding sx={{ display: 'block' }}>
                        <Tooltip title={open ? null : item.text} placement="left">
                            <ListItemButton
                                onClick={() => { navigate(item.path) }}
                                sx={[
                                    {
                                        minHeight: 48,
                                        px: 2.5,
                                        bgcolor: location.pathname === item.path ? theme.palette.mode === 'dark' ? grey[800] : grey[300] : null
                                    },
                                    open
                                        ? {
                                            justifyContent: 'initial',
                                        }
                                        : {
                                            justifyContent: 'center',
                                        },
                                ]}
                            >
                                <ListItemIcon
                                    sx={[
                                        {
                                            minWidth: 0,
                                            justifyContent: 'center',
                                        },
                                        open
                                            ? {
                                                mr: 3,
                                            }
                                            : {
                                                mr: 'auto',
                                            },
                                    ]}
                                >
                                    {item.icon}
                                </ListItemIcon>
                                <ListItemText
                                    primary={item.text}
                                    sx={[
                                        open
                                            ? {
                                                opacity: 1,
                                            }
                                            : {
                                                opacity: 0,
                                            },
                                    ]}
                                />
                            </ListItemButton>
                        </Tooltip>
                    </ListItem>
                ))}
            </List>

            <Divider />

            <List>
                {Array3.map((item) => (
                    <ListItem key={item.path} disablePadding sx={{ display: 'block' }}>
                        <Tooltip title={open ? null : item.text} placement="left">
                            <ListItemButton
                                onClick={() => { navigate(item.path) }}
                                sx={[
                                    {
                                        minHeight: 48,
                                        px: 2.5,
                                        bgcolor: location.pathname === item.path ? theme.palette.mode === 'dark' ? grey[800] : grey[300] : null
                                    },
                                    open
                                        ? {
                                            justifyContent: 'initial',
                                        }
                                        : {
                                            justifyContent: 'center',
                                        },
                                ]}
                            >
                                <ListItemIcon
                                    sx={[
                                        {
                                            minWidth: 0,
                                            justifyContent: 'center',
                                        },
                                        open
                                            ? {
                                                mr: 3,
                                            }
                                            : {
                                                mr: 'auto',
                                            },
                                    ]}
                                >
                                    {item.icon}
                                </ListItemIcon>
                                <ListItemText
                                    primary={item.text}
                                    sx={[
                                        open
                                            ? {
                                                opacity: 1,
                                            }
                                            : {
                                                opacity: 0,
                                            },
                                    ]}
                                />
                            </ListItemButton>
                        </Tooltip>
                    </ListItem>
                ))}
            </List>

        </Drawer >
    )
}

export default Sidebar
