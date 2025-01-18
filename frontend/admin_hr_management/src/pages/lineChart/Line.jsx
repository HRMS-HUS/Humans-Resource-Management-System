import { Box, CircularProgress, useTheme } from '@mui/material'
import { ResponsiveLine } from '@nivo/line'
import axios from 'axios';
import Header from '../../components/Header';
import { useEffect, useState } from 'react';
import { useAuthStore } from '../login/authStore';

const Line = ({ isDashboard = false }) => {

    const theme = useTheme()
    const { token } = useAuthStore()
    const [chartData, setChartData] = useState([]);
    const [loading, setLoading] = useState(false)

    const fetchFinancialInformation = async () => {
        setLoading(true);
        try {

            const [personalInfoResponse, departmentResponse, financialResponse] = await Promise.all([
                axios.get('http://52.184.86.56:8000/api/admin/personal_info', {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                }),
                axios.get('http://52.184.86.56:8000/api/admin/department', {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                }),
                axios.get('http://52.184.86.56:8000/api/admin/financial_info', {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                }),
            ]);

            const personalInfo = personalInfoResponse.data;
            const departments = departmentResponse.data;
            const financialData = financialResponse.data;

            const userDepartmentMap = personalInfo.reduce((map, user) => {
                map[user.user_id] = user.department_id;
                return map;
            }, {});

            const departmentNameMap = departments.reduce((map, department) => {
                map[department.department_id] = department.department_name;
                return map;
            }, {});

            const departmentTotals = {};

            for (const record of financialData) {
                const departmentId = userDepartmentMap[record.user_id];
                if (!departmentId) continue;

                if (!departmentTotals[departmentId]) {
                    departmentTotals[departmentId] = {
                        department_id: departmentId,
                        allowancePhoneBill: 0,
                        allowanceFuel: 0,
                        deductionOther: 0,
                        allowanceSpecial: 0,
                        allowanceMedical: 0,
                        allowanceOther: 0,
                        deductionProvidentFund: 0,
                        deductionTax: 0,
                        allowanceHouseRent: 0,
                        deductionTotal: 0,
                        allowanceTotal: 0,
                    };
                }

                Object.keys(departmentTotals[departmentId]).forEach((key) => {
                    if (key !== 'department_id') {
                        departmentTotals[departmentId][key] += record[key] || 0;
                    }
                });
            }

            const finalData = Object.keys(departmentTotals[Object.keys(departmentTotals)[0]])
                .filter((key) => key !== 'department_id')
                .map((key) => ({
                    id: key,
                    color: `hsl(${Math.floor(Math.random() * 360)}, 70%, 50%)`,
                    data: Object.keys(departmentTotals).map((departmentId) => ({
                        x: departmentNameMap[departmentId] || "Unknown",
                        y: departmentTotals[departmentId][key] || 0,
                    })),
                }));

            return finalData;
        } catch (error) {
            console.error("Error fetching financial information:", error);
            return [];
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        const fetchData = async () => {
            const data = await fetchFinancialInformation();
            setChartData(data);
        };
        fetchData();
    }, []);

    return (
        <Box sx={{ height: isDashboard ? "400px" : "75vh" }}>
            {!isDashboard && (
                <Header title={"Allowance and Deduction of Department"} subTitle={"Total Allowance and Deduction per Department in Company"} />
            )}
            {loading ? (
                <Box sx={{ position: 'absolute', top: '50%', left: '50%', transform: 'translate(-50%, -50%)', }}>
                    <CircularProgress />
                </Box>
            ) : (
                <ResponsiveLine
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
                                    "fill": theme.palette.text.secondary,
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
                                    "fill": theme.palette.text.secondary,
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
                    curve="catmullRom"
                    margin={{ top: 50, right: 165, bottom: 50, left: 70 }}
                    xScale={{ type: 'point' }}
                    yScale={{
                        type: 'linear',
                        min: 'auto',
                        max: 'auto',
                        stacked: true,
                        reverse: false
                    }}
                    yFormat=" >-.2f"
                    axisTop={null}
                    axisRight={null}
                    axisBottom={{
                        tickSize: 5,
                        tickPadding: 0,
                        tickRotation: 0,
                        legend: isDashboard ? null : 'Departments',
                        legendOffset: 38,
                        legendPosition: 'middle',
                        truncateTickAt: 0
                    }}
                    axisLeft={isDashboard ? null : {
                        tickSize: 5,
                        tickPadding: 5,
                        tickRotation: -50,
                        legend: isDashboard ? null : 'Total Allowance and Deduction',
                        legendOffset: -60,
                        legendPosition: 'middle',
                        truncateTickAt: 0
                    }}
                    pointSize={10}
                    pointColor={{ theme: 'background' }}
                    pointBorderWidth={2}
                    pointBorderColor={{ from: 'serieColor' }}
                    pointLabel="data.yFormatted"
                    pointLabelYOffset={-12}
                    enableTouchCrosshair={true}
                    useMesh={true}
                    legends={[
                        {
                            anchor: 'bottom-right',
                            direction: 'column',
                            justify: false,
                            translateX: 100,
                            translateY: 0,
                            itemsSpacing: 0,
                            itemDirection: 'left-to-right',
                            itemWidth: 80,
                            itemHeight: 20,
                            itemOpacity: 0.75,
                            symbolSize: 12,
                            symbolShape: 'circle',
                            symbolBorderColor: 'rgba(0, 0, 0, .5)',
                            effects: [
                                {
                                    on: 'hover',
                                    style: {
                                        itemBackground: 'rgba(0, 0, 0, .03)',
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

export default Line
