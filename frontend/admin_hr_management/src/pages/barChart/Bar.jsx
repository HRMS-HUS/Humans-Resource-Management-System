import { Box, CircularProgress, useTheme } from '@mui/material';
import { ResponsiveBar } from '@nivo/bar';
import axios from 'axios';
import Header from '../../components/Header';
import { useEffect, useState } from 'react';
import { useAuthStore } from '../login/authStore';

const Bar = ({ isDashboard = false }) => {
    const theme = useTheme();
    const { token } = useAuthStore();
    const [loading, setLoading] = useState(false);
    const [data, setData] = useState([]);

    const fetchFinancialInformation = async () => {
        setLoading(true);
        try {

            const [financialResponse, personalResponse, departmentResponse] = await Promise.all([
                axios.get('http://52.184.86.56:8000/api/admin/financial_info', {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                }),
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

            const financialData = financialResponse.data;
            const personalData = personalResponse.data;
            const departmentData = departmentResponse.data;

            const userToDepartmentMap = {};
            personalData.forEach(person => {
                userToDepartmentMap[person.user_id] = person.department_id;
            });

            const departmentIdToNameMap = {};
            departmentData.forEach(department => {
                departmentIdToNameMap[department.department_id] = department.department_name;
            });

            const departmentTotals = {};

            financialData.forEach(record => {
                const departmentId = userToDepartmentMap[record.user_id];
                const departmentName = departmentIdToNameMap[departmentId] || "Unknown Department";

                if (!departmentTotals[departmentName]) {
                    departmentTotals[departmentName] = {
                        totalNetSalary: 0,
                    };
                }

                departmentTotals[departmentName].totalNetSalary += record.salaryNet;
            });

            const departmentDataForDisplay = Object.keys(departmentTotals).map(departmentName => ({
                department_name: departmentName,
                Total_net_Salary: departmentTotals[departmentName].totalNetSalary,
            }));

            setData(departmentDataForDisplay);

        } catch (error) {
            console.error("Error fetching financial information:", error);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchFinancialInformation();
    }, []);

    return (
        <Box sx={{ height: isDashboard ? "250px" : "75vh" }}>
            {!isDashboard && (
                <Header title={"Salary of Department"} subTitle={"Total Net Salary per Department in Company"} />
            )}
            {loading ? (
                <Box sx={{ position: 'absolute', top: '50%', left: '50%', transform: 'translate(-50%, -50%)', }}>
                    <CircularProgress />
                </Box>
            ) : (
                <ResponsiveBar
                    data={data}
                    keys={['Total_net_Salary']}
                    indexBy="department_name"
                    groupMode="grouped"
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
                    margin={{ top: 50, right: 130, bottom: 50, left: 60 }}
                    padding={0.3}
                    valueScale={{ type: 'linear' }}
                    indexScale={{ type: 'band', round: true }}
                    colors={{ scheme: 'paired' }}
                    axisTop={null}
                    axisRight={null}
                    axisBottom={isDashboard ? null : {
                        tickSize: 5,
                        tickPadding: 0,
                        tickRotation: 0,
                        legend: isDashboard ? null : 'Department',
                        legendPosition: 'middle',
                        legendOffset: 40,
                    }}
                    axisLeft={isDashboard ? null : {
                        tickSize: 5,
                        tickPadding: 0,
                        tickRotation: -50,
                        legend: isDashboard ? null : 'Net Salary',
                        legendPosition: 'middle',
                        legendOffset: -55,
                    }}
                    enableLabel={isDashboard ? false : true}
                    labelSkipWidth={12}
                    labelSkipHeight={12}
                    labelTextColor={{
                        from: 'color',
                        modifiers: [
                            ['darker', 1.6]
                        ]
                    }}
                    legends={[
                        {
                            dataFrom: 'keys',
                            anchor: 'bottom-right',
                            direction: 'column',
                            justify: false,
                            translateX: 102,
                            translateY: 0,
                            itemsSpacing: 2,
                            itemWidth: 100,
                            itemHeight: 20,
                            itemDirection: 'left-to-right',
                            itemOpacity: 0.85,
                            symbolSize: 20,
                            effects: [
                                {
                                    on: 'hover',
                                    style: {
                                        itemOpacity: 1
                                    }
                                }
                            ]
                        }
                    ]}
                    role="application"
                    ariaLabel="Nivo bar chart demo"
                    barAriaLabel={e => e.id + ": " + e.formattedValue + " in department: " + e.indexValue}
                />
            )}
        </Box>
    )
}

export default Bar;
