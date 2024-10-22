import React, { useState, useEffect, useContext } from "react";
import { useTheme } from "@mui/material";
import { AgFinancialCharts } from "ag-charts-react";
import { AgCharts as AgChartsEnterprise } from "ag-charts-enterprise";
import useAxios from '@utils/useAxios';

AgChartsEnterprise.setLicenseKey(import.meta.env.VITE_AG_CHART);
console.log(import.meta.env.VITE_AG_CHART)
import "ag-charts-enterprise";
import getData from '@assets/data/stockData'
import StockContext from "@context/StockContext";

const StockAgChart = () => {
  const theme = useTheme();
  const stock = useAxios();
  const [stockData, setStockData] = useState([]);
  const [company, setCompany] = useState("");
  const { stockSymbol } = useContext(StockContext);

  useEffect(() => {
    const fetchStockTracking = async () => {
      console.log(`Stock char ${stockSymbol}`)
      try {
        const res = await stock.post("/stock/stocktracking/historicaldata/", {
          symbol: stockSymbol, 
        });
        
        const formattedData = res.data.price_data.map(item => ({
          ...item,
          date: new Date(item.date), // Chuyển chuỗi thành Date object
          // open: parseFloat(item.open),
          // high: parseFloat(item.high),
          // low: parseFloat(item.low),
          // close: parseFloat(item.close),
          // volume: parseInt(item.volume, 10),
        }))
        console.log(res.data)
        setCompany(res.data.company)
        // .filter(item => 
        //   item.high >= Math.max(item.open, item.close, item.low) &&
        //   item.low <= Math.min(item.open, item.close, item.high) 
        // );
        
        setStockData(formattedData);
        // setName(res.data.company);
      } catch (error) {
        console.error('Có lỗi xảy ra khi truy cập dữ liệu:', error);
      }
    };

    fetchStockTracking();
  }, [stockSymbol]); 

//   useEffect(() => {
//     const socket = new WebSocket('ws://localhost:8001/ws/stocks/');

//     socket.onopen = () => {
//         console.log('WebSocket connection established');
//     };

//     socket.onmessage = (event) => {
//         const data = JSON.parse(event.data);
//         const formattedStockData = data.map(item => ({
//           ...item,
//           date: new Date(item.date) ,
//           open: item.open * 10,       
//           high: item.high * 10,        
//           low: item.low * 10,          
//           close: item.close * 10,
//         }));
//         setStockData(prevData => [...prevData, ...formattedStockData]); 
//         console.log('Received data:', data);
//     };

//     socket.onclose = () => {
//         console.log('WebSocket connection closed');
//     };

//     return () => {
//         socket.close();
//     };
// }, []);

  const [options, setOptions] = useState({
    data: stockData,  
    // data: getData(),  
    title: { text: `${company} .Inc` },
    theme: 'ag-financial',
    navigator: true,
    toolbar: true,
    rangeButtons: true,
    volume: true,
    statusBar: true,
    zoom: true,
    width: 855,
    height: 412,
  });

  useEffect(() => {
    setOptions((prevOptions) => ({
      ...prevOptions,
      title: { text: `${company} .Inc` },
      data: stockData,  
    }));
  }, [stockData]);

  useEffect(() => {
    setOptions((prevOptions) => ({
      ...prevOptions,
      theme: 'ag-sheets',
    }));
  }, [theme.palette.mode]);

  return <AgFinancialCharts options={options} />;
};

export default StockAgChart;
