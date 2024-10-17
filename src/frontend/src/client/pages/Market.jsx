import React, { useRef, useState, useEffect } from "react";
import Helmet from "@client/components/Helmet/Helmet";
import { Container, Row } from "reactstrap";
import { Box, Button, Typography, Icon } from "@mui/material";
import "@client/styles/about.css";
import CandleStickChartWithBollingerBandOverlay from "@client/components/UI/CandleStickChartWithBollingerBandOverlay";
import getData from "@assets/data/stockData"
import BollingerStock from "@client/components/UI/BollingerStock";
import TableComponent from "@client/components/UI/TableComponent";
import TickerDropdown from "@client/components/UI/TickerDropdown";
import ChatIcon from '@mui/icons-material/Chat'; // Import icon Chat
import { useNavigate } from "react-router-dom"; // Điều hướng
import StockAgChart from "@client/components/UI/StockAgChart";
const Market = () => {
    const boxRef = useRef(null);
    const [chartWidth, setChartWidth] = useState(0);
    const navigate = useNavigate();

    useEffect(() => {
        const handleResize = () => {
            if (boxRef.current) {
                setChartWidth(boxRef.current.offsetWidth);
            }
        };

        handleResize(); // Set initial width

        window.addEventListener('resize', handleResize);

        return () => window.removeEventListener('resize', handleResize);
    }, []);

    return (
        <Helmet title="Stock Analysis">
            <section className="about__page-section" style={{ backgroundColor: '#fff' }}>
                <Container>
                    <Row>
                        <div>This is stock market</div>
                        <Box
                            display="grid"
                            gridTemplateColumns="repeat(15, 1fr)"
                            gridAutoRows="90px"
                            gap="20px"
                        >
                            {/* Row 1 */}
                               <Box
                                gridColumn="span 3"
                                backgroundColor={"#f0f3f7"}
                                display="flex"
                                alignItems="center"
                                justifyContent="center"
                            >
         
 
                            </Box>
                               <Box
                                gridColumn="span 3"
                                backgroundColor={"#f0f3f7"}
                                display="flex"
                                alignItems="center"
                                justifyContent="center"
                            >
         
 
                            </Box>
                               <Box
                                gridColumn="span 3"
                                backgroundColor={"#f0f3f7"}
                                display="flex"
                                alignItems="center"
                                justifyContent="center"
                            >
         
 
                            </Box>
                               <Box
                                gridColumn="span 3"
                                backgroundColor={"#f0f3f7"}
                                display="flex"
                                alignItems="center"
                                justifyContent="center"
                            >
         
 
                            </Box>
                        {/* <Box
                        gridColumn="span 3"
                        backgroundColor={"#f0f3f7"}
                        display="flex"
                        alignItems="center"
                        justifyContent="center"
                        >
                        <StatBox
                            title={300}
                            subtitle="Transactions"
                            progress="0.50"
                            increase="+21%"
                            icon={
                            <PointOfSaleIcon
                                sx={{ color: "#f0f3f7", fontSize: "26px" }}
                            />
                            }
                        />
                        </Box>
                        <Box
                        gridColumn="span 3"
                        backgroundColor={"#f0f3f7"}
                        display="flex"
                        alignItems="center"
                        justifyContent="center"
                        >
                        <StatBox
                            title={10}
                            subtitle="Quantity Product"
                            progress="0.30"
                            increase="+5%"
                            icon={
                            <ProductionQuantityLimitsIcon
                                sx={{ color: "#f0f3f7", fontSize: "26px" }}
                            />
                            }
                        />
                        </Box> */}
                    
                        <Box
                        gridColumn="span 3"
                        backgroundColor={"#fff"}
                        display="flex"
                        alignItems="center"
                        justifyContent="center"
                        zIndex={10000}
                        >
                        <TickerDropdown/>
                        
                        </Box>
                        {/* <Box
                            gridColumn="span 15"
                            gridRow="span 4"
                            backgroundColor={"#f0f3f7"}
                            // ref={boxRef}
                            display="flex"
                            justifyContent="center"
                            alignItems="center"
                            height="500"
                        >
                            <TableComponent width={550} height={275}/>
                        </Box> */}
                        <Box
                            gridColumn="span 10"
                            gridRow="span 4"
                            backgroundColor={"#f0f3f7"}
                            // ref={boxRef}
                            display="flex"
                            justifyContent="center"
                            alignItems="center"
                            height="450"
                        >
                            <StockAgChart/>
                        </Box>
                        <Box
                            gridColumn="span 5"
                            gridRow="span 4"
                            backgroundColor={"#f0f3f7"}
                            // ref={boxRef}
                            display="flex"
                            justifyContent="center"
                            alignItems="center"
                            height="450"
                        >
                        </Box>
                       
                        <Box
                            gridColumn="span 2"
                            gridRow="span 1"
                            backgroundColor={"#fff"}
                            // ref={boxRef}
                            display="flex"
                            justifyContent="center"
                            alignItems="center"
                            height="450"
                        >
                            <Button
                            variant="contained"
                            color="primary"
                            onClick={() => alert('Prediction clicked!')}
                            sx={{
                                padding: '16px 32px', 
                                fontSize: '14px',     
                                borderRadius: '8px',  
                                fontWeight: 'bold',   
                                backgroundColor: '#3f51b5', 
                                '&:hover': {
                                backgroundColor: '#303f9f', 
                                transform: 'scale(1.05)',   
                                },
                                boxShadow: '0 4px 20px rgba(0, 0, 0, 0.2)', 
                                transition: 'all 0.3s ease', 
                            }}
                            >
                            Prediction
                            </Button>

                        </Box>
                        <Box
                            gridColumn="span 11"
                            gridRow="span 1"
                            backgroundColor={"#fff"}
                            // ref={boxRef}
                            display="flex"
                            justifyContent="center"
                            alignItems="center"
                            height="450"
                        >
                        </Box>
                        <Box
                                    display="flex"
                                    gridColumn="span 2"
                                    gridRow="span 1"
                                    alignItems="center"
                                    sx={{
                                        cursor: "pointer",
                                        color: "orange",
                                        fontWeight: "bold",
                                        '&:hover': {
                                            transform: "scale(1.1)",
                                            color: "#FF8C00", 
                                        },
                                        transition: "all 0.3s ease", 
                                    }}
                                    onClick={() => navigate('/chatbot')} 
                                >
                                    <ChatIcon sx={{ marginRight: "8px" }} /> 
                                    <Typography variant="h4">
                                        Go to Chatbot
                                    </Typography>
                                </Box>
                          
                                    
                       
                    </Box>
                </Row>
        </Container>
    </section>
</Helmet>
    );
};

export default Market;
