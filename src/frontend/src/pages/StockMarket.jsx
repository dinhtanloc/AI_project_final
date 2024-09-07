import React, { useRef, useState, useEffect } from "react";
import StockChart from "@components/UI/StockChart";
import Helmet from "@components/Helmet/Helmet";
import { Container, Row } from "reactstrap";
import { Box } from "@mui/material";
import "@styles/about.css";

const StockMarket = () => {
    const boxRef = useRef(null);
    const [chartWidth, setChartWidth] = useState(0);

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
                            gridTemplateColumns="repeat(12, 1fr)"
                            gridAutoRows="90px"
                            gap="20px"
                        >
                            <Box
                                gridColumn="span 12"
                                gridRow="span 4"
                                backgroundColor={"#f0f3f7"}
                                ref={boxRef}
                                display="flex"
                                justifyContent="center"
                                alignItems="center"
                                height="410px"
                            >
                                <StockChart w={chartWidth - 100} h={390} />
                            </Box>
                        </Box>
                    </Row>
                </Container>
            </section>
        </Helmet>
    );
};

export default StockMarket;
