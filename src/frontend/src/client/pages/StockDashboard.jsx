import React, { useContext, useEffect, useState } from "react";
import ThemeContext from "@context/ThemeContext";
import Overview from "@client/components/UI/StockChart/Overview";
import Details from "@client/components/UI/StockChart/Details";
import Chart from "@client/components/UI/StockChart/Chart";
import Header from "@client/components/UI/StockChart/Header";
import StockContext from "@context/StockContext";
// import { fetchStockDetails, fetchQuote } from "@utils/api/stock-api";
import ChatIcon from '@mui/icons-material/Chat'; // Import icon Chat
import { Box, Button, Typography, Icon } from "@mui/material";
import { useNavigate } from "react-router-dom";
import useAxios from '@utils/useAxios';


const ActionButton = ({ onClick, label }) => (
  <Button
    variant="contained"
    color="primary"
    onClick={onClick}
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
    {label}
  </Button>
);

const StockDashboard = () => {
  const { darkMode } = useContext(ThemeContext);
  const navigate=useNavigate();
  const stock=useAxios();


  const { stockSymbol } = useContext(StockContext);

  const [stockDetails, setStockDetails] = useState({});

  const [quote, setQuote] = useState({});
 

  useEffect(() => {
      // const fetchStockTracking = async () => {
      //   try {
      //     const res = await stock.get("/stock/stocktracking/historicaldata/");
          
      //     const formattedData = res.data.price_data.map(item => ({
      //       ...item,
      //       date: new Date(item.date), // Chuyển chuỗi thành Date object
      //       // open: parseFloat(item.open),
      //       // high: parseFloat(item.high),
      //       // low: parseFloat(item.low),
      //       // close: parseFloat(item.close),
      //       // volume: parseInt(item.volume, 10),
      //     }))
      //     // setName(res.data.company)
      //     // .filter(item => 
      //     //   item.high >= Math.max(item.open, item.close, item.low) &&
      //     //   item.low <= Math.min(item.open, item.close, item.high) 
      //     // );
          
      //     setQuote(formattedData);
      //     // setName(res.data.company);
      //   } catch (error) {
      //     console.error('Có lỗi xảy ra khi truy cập dữ liệu:', error);
      //   }
      // };
  
      // fetchStockTracking();

    const updateStockDetails = async () => {
      try {
        const res = await stock.post("/stock/stocktracking/tracking_stockinformation/", {
          symbol: stockSymbol, 
        });
      // console.log(res.data);
      // setInfo(res.data)
        setStockDetails({
          name: res.data.overview.short_name,
          country: "Việt Nam",
          currency: "VND",
          exchange: res.data.overview.exchange,
          ipo: res.data.overview.established_year,
          marketCapitalization: `${Math.round(res.data.overview.issue_share[0])} triệu`,
          finnhubIndustry: res.data.overview.industry
        });
      } catch (error) {
        setStockDetails({});
        console.log(error);
      }
    };



    updateStockDetails();
  }, []);

  return (
    <div
      className={`h-screen grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 grid-rows-8 md:grid-rows-7 xl:grid-rows-5 auto-rows-fr gap-6 p-10 font-quicksand ${
        darkMode ? "bg-gray-900 text-gray-300" : "bg-neutral-100"
      }`}
    >
      {/* <div className="col-span-1 md:col-span-2 xl:col-span-3 row-span-1 flex justify-start items-center">
        <Header name={stockDetails.name} />
      </div> */}
      <div className="md:col-span-2 row-span-4">
        <Chart />
      </div>
      <div>
        <Overview
          symbol={stockSymbol}
          price={200}
          change={13/12}
          changePercent={"5%"}
          currency={'VND'}
        />
      </div>
      <div className="row-span-2 xl:row-span-3">
        <Details details={stockDetails} />
      </div>
      <div className="col-span-3">
      <Box display="grid" gridTemplateColumns="repeat(15, 1fr)" gridAutoRows="90px" gap="20px">
        <Box gridColumn="span 2" gridRow="span 1" display="flex" justifyContent="center" alignItems="center" height="450">
          <ActionButton onClick={() => navigate('/stock-market')} label="Return" />
        </Box>
        <Box gridColumn="span 11" gridRow="span 1" display="flex" justifyContent="center" alignItems="center" height="450" />
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
          <Typography variant="h4">Go to Chatbot</Typography>
        </Box>
      </Box>
      </div>
    </div>
  );
};

export default StockDashboard;
