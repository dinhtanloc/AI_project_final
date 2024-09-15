import React, { useEffect, useContext,useState } from "react";
import { Box, Button, IconButton, Typography, useTheme } from "@mui/material";
import { tokens } from "@theme";
import DownloadOutlinedIcon from "@mui/icons-material/DownloadOutlined";
import ProductionQuantityLimitsIcon from '@mui/icons-material/ProductionQuantityLimits';
import MonetizationOnIcon from '@mui/icons-material/MonetizationOn';
import PointOfSaleIcon from "@mui/icons-material/PointOfSale";
import PersonAddIcon from "@mui/icons-material/PersonAdd";
import InventoryIcon from '@mui/icons-material/Inventory';
import Header from "./HeaderDashboard";
import numeral from 'numeral';
import useAxios from "@utils/useAxios"
import StockAgChart from "@components/UI/StockAgChart";
// import StockChart from "@components/UI/StockChart"
// import {SummaryLineChart} from "@components/UI/LineChart";
// import GeographyChart from "@components/UI/GeographyChart";
// import BarChart from "@components/UI/BarChart";
import StatBox from "@components/UI/StatBox";
// import ProgressCircle from "@components/UI/ProgressCircle";
// import RecentTransactions from "@components/UI/RecentTransactions";

// import downloadExcel from "../utils/downloadExcel";

const Dashboard = () => {
  // return(
  //   <div>Dashboard page</div>
  // )



  // window.location.reload()
  const theme = useTheme();
  const colors = tokens(theme.palette.mode);
  const [OrderInfo, checkOrderInfo] = useState([]);
  const [ProductInfo, checkProductInfo] = useState([]);
  const [orderRecent,setorderRecent] = useState([]);
  const api = useAxios();
  
  useEffect(() => {
    fetchTotalOrder();
    fetchProductInventory();
    fetchOrderList();
  }, []);

  const handleDownload = async () => {
    // try {
    //     const response = await fetch(`${import.meta.env.VITE_DOMAIN_BACKEND}/orders/download-excel/`, {
    //         method: 'GET',
    //         headers: {
    //             'Content-Type': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    //         },
    //     });

    //     if (!response.ok) {
    //         throw new Error('Network response was not ok');
    //     }

    //     const blob = await response.blob();
    //     const url = window.URL.createObjectURL(new Blob([blob]));
    //     const link = document.createElement('a');
    //     link.href = url;
    //     link.setAttribute('download', 'orders.xlsx');
    //     document.body.appendChild(link);
    //     link.click();
    //     link.parentNode.removeChild(link);
    // } catch (error) {
    //     console.error('Error downloading the file', error);
    // }
};
  



 
  
  return (
    <Box m="20px">
      {/* HEADER */}
      <Box display="flex" justifyContent="space-between" alignItems="center">
        <Header title="DASHBOARD" subtitle="Welcome to your dashboard" />
        <Box>
          <Button
            sx={{
              backgroundColor: colors.blueAccent[700],
              color: colors.grey[100],
              fontSize: "14px",
              fontWeight: "bold",
              padding: "10px 20px",
            }}
            onClick = {handleDownload}
          >
            <DownloadOutlinedIcon sx={{ mr: "10px" }} />
            Download Data
          </Button>
        </Box>
      </Box>

      {/* GRID & CHARTS */}
      <Box
        display="grid"
        gridTemplateColumns="repeat(12, 1fr)"
        gridAutoRows="90px"
        gap="20px"
      >
        {/* ROW 1 */}
        <Box
          gridColumn="span 3"
          backgroundColor={colors.primary[400]}
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
                sx={{ color: colors.greenAccent[600], fontSize: "26px" }}
              />
            }
          />
        </Box>
        <Box
          gridColumn="span 3"
          backgroundColor={colors.primary[400]}
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
                sx={{ color: colors.greenAccent[600], fontSize: "26px" }}
              />
            }
          />
        </Box>
        <Box
          gridColumn="span 3"
          backgroundColor={colors.primary[400]}
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
                sx={{ color: colors.greenAccent[600], fontSize: "26px" }}
              />
            }
          />
        </Box>
        <Box
          gridColumn="span 3"
          backgroundColor={colors.primary[400]}
          display="flex"
          alignItems="center"
          justifyContent="center"
        >
          <StatBox
            title={5}
            subtitle="Out of stock"
            progress="0.80"
            increase="+43%"
            icon={
              <InventoryIcon
                sx={{ color: colors.greenAccent[600], fontSize: "26px" }}
              />
            }
          />
        </Box>
        {/* ROW 2 */}
        <Box
          gridColumn="span 12"
          gridRow="span 4"
          backgroundColor={colors.primary[400]}
        >
       
          <Box height="250px" m="0px 0 0 0">
            <StockAgChart   />
          </Box>
        </Box>
      </Box>
    </Box>
  );
};

export default Dashboard;
