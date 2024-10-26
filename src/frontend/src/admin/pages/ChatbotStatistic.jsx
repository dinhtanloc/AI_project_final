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
import ChatbotAdmin from '@admin/components/UI/ChatbotAdmin'
import ChatbotContextProvider from '@context/ChatbotContext.jsx'
// import downloadExcel from "../utils/downloadExcel";

const ChatbotStatistic = () => {



  // window.location.reload()
  const theme = useTheme();
  const colors = tokens(theme.palette.mode);
  const [OrderInfo, checkOrderInfo] = useState([]);
  const [ProductInfo, checkProductInfo] = useState([]);
  const [orderRecent,setorderRecent] = useState([]);
  const api = useAxios();
  
  
  const handleRedirect = () => {
    window.location.href = 'https://smith.langchain.com/o/02fd074a-1ef8-4483-8d12-ed3c37243258/projects/p/6a26e205-9955-4935-85fa-4a00127e892d?timeModel=%7B%22duration%22%3A%227d%22%7D';
  };
  



 
  
  return (
    <Box m="20px">
      {/* HEADER */}
      <Box display="flex" justifyContent="space-between" alignItems="center">
        <Header title="Chatbot" subtitle="Evaluate and improve model chatbot" />
        <Box>
          <Button
            sx={{
              backgroundColor: colors.blueAccent[700],
              color: colors.grey[100],
              fontSize: "14px",
              fontWeight: "bold",
              padding: "10px 20px",
            }}
            onClick = {handleRedirect}
          >
            <DownloadOutlinedIcon sx={{ mr: "10px" }} />
            Performance
          </Button>
        </Box>
      </Box>

      <ChatbotContextProvider>
        <ChatbotAdmin />
      </ChatbotContextProvider>

    </Box>
  );
};

export default ChatbotStatistic;
