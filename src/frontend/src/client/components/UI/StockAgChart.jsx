import React, { useState, useEffect, useContext } from "react";
import { useTheme } from "@mui/material";
import { AgFinancialCharts } from "ag-charts-react";
import { AgCharts as AgChartsEnterprise } from "ag-charts-enterprise";
import useAxios from '@utils/useAxios';

AgChartsEnterprise.setLicenseKey(import.meta.env.VITE_AG_CHART);
import "ag-charts-enterprise";
import StockContext from "@context/StockContext";

const StockAgChart = () => {
  const theme = useTheme();
  const stock = useAxios();
  const [stockData, setStockData] = useState([]);
  const [company, setCompany] = useState("");
  const { stockSymbol } = useContext(StockContext);

  useEffect(() => {
    const fetchStockTracking = async () => {
      try {
        const res = await stock.post("/stock/stocktracking/historicaldata/", {
          symbol: stockSymbol, 
        });
        
        const formattedData = res.data.price_data.map(item => ({
          ...item,
          date: new Date(item.date), 
          
        }))
        setCompany(res.data.company)
        
        
        setStockData(formattedData);
      } catch (error) {
        console.error('Có lỗi xảy ra khi truy cập dữ liệu:', error);
      }
    };

    fetchStockTracking();
  }, [stockSymbol]); 



  const [options, setOptions] = useState({
    data: stockData,  
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
