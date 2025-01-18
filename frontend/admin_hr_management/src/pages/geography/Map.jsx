import { Box, CircularProgress, useTheme } from '@mui/material'
import { ResponsiveChoropleth } from '@nivo/geo'
import axios from 'axios'
import { world_countries } from '../../pages/information/data'
import { useEffect, useState } from 'react'
import { geo } from './world_countries'
import { useAuthStore } from '../login/authStore';

const Map = ({ isDashboard = false }) => {

    const theme = useTheme()
    const [projectionScale, setProjectionScale] = useState(isDashboard ? 70 : 150);
    const [projectionTranslation, setProjectionTranslation] = useState([0.5, 0.5]);
    const [dragging, setDragging] = useState(false);
    const [startPosition, setStartPosition] = useState([0, 0]);
    const [data, setData] = useState([])
    const { token } = useAuthStore()
    const [loading, setLoading] = useState(false)

    const fetchCountry = async () => {
        setLoading(true)
        try {
            const response = await axios.get('http://52.184.86.56:8000/api/admin/personal_info', {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            });
            const countryCounts = response.data.reduce((acc, item) => {
                const country = world_countries.find(country => country.label === item.country);
                if (country) {
                    const id = country.id;
                    acc[id] = (acc[id] || 0) + 1;
                }
                return acc;
            }, {});

            const formattedData = Object.keys(countryCounts).map(id => ({
                'id': id,
                'value': countryCounts[id]
            }));
            setData(formattedData);
        } catch (error) {
            console.error("Error fetching number of employee", error);
            return "Error";
        } finally {
            setLoading(false)
        }
    };

    useEffect(() => {
        fetchCountry();
    }, []);

    const handleWheel = (event) => {
        event.preventDefault();
        setProjectionScale((prevScale) => {
            const newScale = prevScale - event.deltaY * 0.1;
            return Math.max(50, Math.min(newScale, 500));
        });
    };

    const handleMouseDown = (event) => {
        if (isDashboard) return;
        setDragging(true);
        setStartPosition([event.clientX, event.clientY]);
    };

    const handleMouseMove = (event) => {
        if (!dragging || isDashboard) return;

        const [startX, startY] = startPosition;
        const deltaX = (event.clientX - startX) / window.innerWidth;
        const deltaY = (event.clientY - startY) / window.innerHeight;

        setProjectionTranslation(([x, y]) => [
            Math.max(0, Math.min(1, x + deltaX)),
            Math.max(0, Math.min(1, y + deltaY)),
        ]);

        setStartPosition([event.clientX, event.clientY]);
    };

    const handleMouseUp = () => { setDragging(false); };

    return (
        <Box
            onMouseDown={!isDashboard ? handleMouseDown : null}
            onMouseMove={!isDashboard ? handleMouseMove : null}
            onMouseUp={!isDashboard ? handleMouseUp : null}
            onMouseLeave={!isDashboard ? handleMouseUp : null}
            onWheel={isDashboard ? null : handleWheel}
            sx={{ borderRadius: "5px", height: isDashboard ? "380px" : "85vh", border: isDashboard ? null : `1px solid ${theme.palette.text.primary}` }}
        >
            {loading ? (
                <Box sx={{ position: 'absolute', top: '50%', left: '50%', transform: 'translate(-50%, -50%)', }}>
                    <CircularProgress />
                </Box>
            ) : (
                <ResponsiveChoropleth
                    projectionScale={projectionScale}
                    // @ts-ignore
                    projectionTranslation={projectionTranslation}
                    data={data}
                    features={geo.features}
                    margin={{ top: 0, right: 0, bottom: 0, left: 0 }}
                    colors="spectral"
                    domain={[0, Math.max(...data.map(item => item.value)) > 11 ? Math.max(...data.map(item => item.value)) : 11]}
                    unknownColor="#666666"
                    label="properties.name"
                    valueFormat=".2s"
                    projectionRotation={[0, 0, 0]}
                    enableGraticule={false}
                    graticuleLineColor="#dddddd"
                    borderWidth={1.1}
                    borderColor="#fff"
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
                    legends={isDashboard ? [] : [
                        {
                            anchor: 'bottom-left',
                            direction: 'column',
                            justify: true,
                            translateX: 20,
                            translateY: -20,
                            itemsSpacing: 0,
                            itemWidth: 94,
                            itemHeight: 18,
                            itemDirection: 'left-to-right',
                            itemTextColor: theme.palette.text.primary,
                            itemOpacity: 0.85,
                            symbolSize: 18,
                            effects: [
                                {
                                    on: 'hover',
                                    style: {
                                        itemTextColor: '#000000',
                                        itemOpacity: 1
                                    }
                                }
                            ]
                        }
                    ]}
                />
            )}
        </Box>
    )
}

export default Map
