import { Box, CircularProgress, useTheme } from '@mui/material'
import { ResponsivePie } from '@nivo/pie'
import axios from 'axios'
import Header from '../../components/Header';
import { useEffect, useState } from 'react'
import { useAuthStore } from '../login/authStore';

const Pie = ({ isDashboard = false }) => {

    const theme = useTheme()
    const [chartData, setChartData] = useState([]);
    const { token } = useAuthStore()
    const [loading, setLoading] = useState(false)

    const fetchData = async () => {
        setLoading(true)
        try {
            const [response1, response2] = await Promise.all([
                axios.get('http://52.184.86.56:8000/api/admin/personal_info', {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                }),
                axios.get('http://52.184.86.56:8000/api/admin/department', {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                })
            ]);

            const groupedData = response1.data.reduce((acc, curr) => {
                const department = curr.department_id;
                if (!acc[department]) {
                    acc[department] = 1;
                } else {
                    acc[department]++;
                }
                return acc;
            }, {});

            const formattedData = Object.keys(groupedData).map((key) => {
                const department = response2.data.find(dept => dept.department_id === key);
                return {
                    id: department ? `${key} - ${department.department_name}` : key,
                    label: key,
                    value: groupedData[key],
                };
            });

            setChartData(formattedData);
        } catch (error) {
            console.error("Error fetching data:", error);
        } finally {
            setLoading(false)
        }
    };

    useEffect(() => {
        fetchData();
    }, []);

    return (
        <div>
            <Box sx={{ height: isDashboard ? "220px" : "75vh" }}>
                {!isDashboard && (
                    <Header title={"Employees of Department"} subTitle={"Number of Employees per Department in Company"} />
                )}
                {loading ? (
                    <Box sx={{ position: 'absolute', top: '50%', left: '50%', transform: 'translate(-50%, -50%)', }}>
                        <CircularProgress />
                    </Box>
                ) : (
                    <ResponsivePie
                        data={chartData}
                        theme={{
                            "text": {
                                "fontSize": 11,
                                "fill": theme.palette.text.primary,
                                "outlineWidth": 0,
                                "outlineColor": "transparent"
                            },
                            "axis": {
                                "domain": {
                                    "line": {
                                        "stroke": theme.palette.divider,
                                        "strokeWidth": 1
                                    }
                                },
                                "legend": {
                                    "text": {
                                        "fontSize": 12,
                                        "fill": theme.palette.text.primary,
                                        "outlineWidth": 0,
                                        "outlineColor": "transparent"
                                    }
                                },
                                "ticks": {
                                    "line": {
                                        "stroke": theme.palette.divider,
                                        "strokeWidth": 1
                                    },
                                    "text": {
                                        "fontSize": 11,
                                        "fill": theme.palette.text.primary,
                                        "outlineWidth": 0,
                                        "outlineColor": "transparent"
                                    }
                                }
                            },
                            "grid": {
                                "line": {
                                    "stroke": theme.palette.divider,
                                    "strokeWidth": 1
                                }
                            },
                            "legends": {
                                "title": {
                                    "text": {
                                        "fontSize": 11,
                                        "fill": theme.palette.text.primary,
                                        "outlineWidth": 0,
                                        "outlineColor": "transparent"
                                    }
                                },
                                "text": {
                                    "fontSize": 11,
                                    "fill": theme.palette.text.primary,
                                    "outlineWidth": 0,
                                    "outlineColor": "transparent"
                                },
                                "ticks": {
                                    "line": {},
                                    "text": {
                                        "fontSize": 10,
                                        "fill": theme.palette.text.primary,
                                        "outlineWidth": 0,
                                        "outlineColor": "transparent"
                                    }
                                }
                            },
                            "annotations": {
                                "text": {
                                    "fontSize": 13,
                                    "fill": theme.palette.text.primary,
                                    "outlineWidth": 2,
                                    "outlineColor": "#ffffff",
                                    "outlineOpacity": 1
                                },
                                "link": {
                                    "stroke": "#000000",
                                    "strokeWidth": 1,
                                    "outlineWidth": 2,
                                    "outlineColor": "#ffffff",
                                    "outlineOpacity": 1
                                },
                                "outline": {
                                    "stroke": "#000000",
                                    "strokeWidth": 2,
                                    "outlineWidth": 2,
                                    "outlineColor": "#ffffff",
                                    "outlineOpacity": 1
                                },
                                "symbol": {
                                    "fill": "#000000",
                                    "outlineWidth": 2,
                                    "outlineColor": "#ffffff",
                                    "outlineOpacity": 1
                                }
                            },
                            "tooltip": {
                                "wrapper": {},
                                "container": {
                                    "background": theme.palette.background.default,
                                    "color": theme.palette.text.primary,
                                    "fontSize": 12
                                },
                                "basic": {},
                                "chip": {},
                                "table": {},
                                "tableCell": {},
                                "tableCellValue": {}
                            }
                        }}
                        margin={isDashboard ?
                            { top: 10, right: 0, bottom: 10, left: 0 } :
                            { top: 30, right: 60, bottom: 60, left: 60 }
                        }
                        innerRadius={isDashboard ? 0.8 : 0.5}
                        padAngle={0.7}
                        cornerRadius={3}
                        activeOuterRadiusOffset={8}
                        borderWidth={1}
                        borderColor={{
                            from: 'color',
                            modifiers: [
                                [
                                    'darker',
                                    0.2
                                ]
                            ]
                        }}
                        arcLinkLabelsSkipAngle={10}
                        arcLinkLabelsTextColor={theme.palette.text.primary}
                        arcLinkLabelsThickness={2}
                        arcLinkLabelsColor={{ from: 'color' }}
                        arcLabelsSkipAngle={10}

                        enableArcLabels={isDashboard ? false : true}
                        enableArcLinkLabels={isDashboard ? false : true}

                        arcLabelsTextColor={{
                            from: 'color',
                            modifiers: [
                                [
                                    'darker',
                                    2
                                ]
                            ]
                        }}
                        defs={[
                            {
                                id: 'dots',
                                type: 'patternDots',
                                background: 'inherit',
                                color: theme.palette.text.primary,
                                size: 4,
                                padding: 1,
                                stagger: true
                            },
                            {
                                id: 'lines',
                                type: 'patternLines',
                                background: 'inherit',
                                color: theme.palette.text.primary,
                                rotation: -45,
                                lineWidth: 6,
                                spacing: 10
                            }
                        ]}
                        legends={
                            isDashboard ? [] :
                                [
                                    {
                                        anchor: 'bottom',
                                        direction: 'row',
                                        justify: false,
                                        translateX: 0,
                                        translateY: 56,
                                        itemsSpacing: 0,
                                        itemWidth: 100,
                                        itemHeight: 18,
                                        itemTextColor: theme.palette.text.primary,
                                        itemDirection: 'left-to-right',
                                        itemOpacity: 1,
                                        symbolSize: 18,
                                        symbolShape: 'circle',
                                        effects: [
                                            {
                                                on: 'hover',
                                                style: {
                                                    itemTextColor: theme.palette.text.primary
                                                }
                                            }
                                        ]
                                    }
                                ]}
                    />
                )}
            </Box>
        </div >
    )
}

export default Pie
