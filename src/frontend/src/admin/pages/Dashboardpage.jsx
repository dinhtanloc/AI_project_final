import React, { useEffect, useContext,useState } from "react";
import { Box, Button, useTheme } from "@mui/material";
import { tokens } from "@theme";
import DownloadOutlinedIcon from "@mui/icons-material/DownloadOutlined";
import ProductionQuantityLimitsIcon from '@mui/icons-material/ProductionQuantityLimits';
import MonetizationOnIcon from '@mui/icons-material/MonetizationOn';
import PointOfSaleIcon from "@mui/icons-material/PointOfSale";
import InventoryIcon from '@mui/icons-material/Inventory';
import Header from "./HeaderDashboard";
import useAxios from "@utils/useAxios"
import StockAgChart from "@admin/components/UI/StockAgChart";
import StatBox from "@admin/components/UI/StatBox";

// import downloadExcel from "../utils/downloadExcel";

const Dashboard = () => {



  // window.location.reload()
  const theme = useTheme();
  const colors = tokens(theme.palette.mode);

  
  

  



 
  
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
          >
            <DownloadOutlinedIcon sx={{ mr: "10px" }} />
            Download Data
          </Button>
        </Box>
      </Box>

     
    </Box>
  );
};

export default Dashboard;
