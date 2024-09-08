import React, { useRef, useState, useEffect } from "react";
// import StockChart from "@components/UI/StockChart";
import Helmet from "@components/Helmet/Helmet";
import { Container, Row } from "reactstrap";
import { Box, Button, IconButton, Typography, useTheme } from "@mui/material";
import StatBox from "@components/UI/StatBox";
import { tokens } from "@theme";
import DownloadOutlinedIcon from "@mui/icons-material/DownloadOutlined";
import ProductionQuantityLimitsIcon from '@mui/icons-material/ProductionQuantityLimits';
import MonetizationOnIcon from '@mui/icons-material/MonetizationOn';
import PointOfSaleIcon from "@mui/icons-material/PointOfSale";
import PersonAddIcon from "@mui/icons-material/PersonAdd";
import InventoryIcon from '@mui/icons-material/Inventory';
// import { Box } from "@mui/material";
import "@styles/about.css";
import CandleStickChartWithBollingerBandOverlay from "@components/UI/CandleStickChartWithBollingerBandOverlay";
import getData from "@assets/data/stockData"
import BollingerStock from "@components/UI/BollingerStock";
import TableComponent from "@components/UI/TableComponent";
import TickerDropdown from "@components/UI/TickerDropdown";


const StockMarket = () => {
    const boxRef = useRef(null);
    const [n, setN] = useState(20); // Periods
    const [k, setK] = useState(2);
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
          <StatBox
            title="70000"
            subtitle="Total sale"
            progress="0.75"
            increase="+14%"
            icon={
              <MonetizationOnIcon
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
        </Box>
        <Box
          gridColumn="span 3"
          backgroundColor={"#f0f3f7"}
          display="flex"
          alignItems="center"
          justifyContent="center"
        >
          <TickerDropdown/>
          {/* <StatBox
            title={5}
            subtitle="Out of stock"
            progress="0.80"
            increase="+43%"
            icon={
              <InventoryIcon
                sx={{ color: "#f0f3f7", fontSize: "26px" }}
              />
            }
          /> */}
        </Box>
        <Box
          gridColumn="span 3"
          backgroundColor={"#f0f3f7"}
          display="flex"
          flexDirection="column"
          alignItems="center"
          justifyContent="center"
          gap="10px"
        //   padding="0px"
        >
            <div>
        <label style={{color:"black", marginRight:'14px'}}>Periods (N):</label>
        <input
          type="range"
          min="2"
          max="100"
          step="1"
          value={n}
          onChange={(e) => setN(Number(e.target.value))}
        />
        {/* <span>{n}</span> */}
      </div>
      <div>
        <label style={{color:"black",marginRight:'2px'}}>Deviations (K):</label>
        <input
          type="range"
          min="0"
          max="4"
          step="0.1"
          value={k}
          onChange={(e) => setK(Number(e.target.value))}
        />
        {/* <span>{k}</span> */}
      </div>
         
        </Box>
        {/* Row 2 */}
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
                                {/* <StockChart w={chartWidth - 100} h={390} /> */}
                                <CandleStickChartWithBollingerBandOverlay data={getData()} width={980} ratio={1}/>
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
                            ></Box>
                            {/* Row 3 */}
                            <Box
                                gridColumn="span 9"
                                gridRow="span 3"
                                backgroundColor={"#f0f3f7"}
                                display="flex"
                                justifyContent="center"
                                alignItems="center"
                                height="500"
                            >
                                {/* <StockChart w={chartWidth - 100} h={390} /> */}
                                {/* <CandleStickChartWithBollingerBandOverlay data={getData()} width={1200} ratio={1}/> */}
                                <BollingerStock/>
                            </Box>
                            <Box
                                gridColumn="span 6"
                                gridRow="span 3"
                                backgroundColor={"#f0f3f7"}
                                // ref={boxRef}
                                display="flex"
                                justifyContent="center"
                                alignItems="center"
                                height="500"
                            >
                              <TableComponent width={550} height={275}/>
                            </Box>
                        </Box>
                    </Row>
                </Container>
            </section>
        </Helmet>
    );
};

export default StockMarket;
