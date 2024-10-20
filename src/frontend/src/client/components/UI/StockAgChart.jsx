import React, { useState, useEffect } from "react";
import { useTheme } from "@mui/material";
import { AgFinancialCharts } from "ag-charts-react";
import { AgCharts as AgChartsEnterprise } from "ag-charts-enterprise";
import useAxios from '@utils/useAxios';

AgChartsEnterprise.setLicenseKey(import.meta.env.VITE_AG_CHART);
import "ag-charts-enterprise";
import getData from "@assets/data/stockData"

const StockAgChart = () => {
  const theme = useTheme();
  const stock = useAxios();
  const [stockData, setStockData] = useState([]);
  const [name, setName] = useState("ACB");

  // Hàm fetch dữ liệu
  const fetchStockTracking = async () => {
    try {
      const res = await stock.get("/stock/stocktracking/tracking_stockprice/");

      const formattedData = res.data.price_data.map(item => ({
        ...item,
        date: new Date(item.date),
        open: parseFloat(item.open),
        high: parseFloat(item.high),
        low: parseFloat(item.low),
        close: parseFloat(item.close),
        volume: parseInt(item.volume, 10),
      })).filter(item => 
        item.high >= Math.max(item.open, item.close, item.low) &&
        item.low <= Math.min(item.open, item.close, item.high) // Đảm bảo giá trị 'low' hợp lệ
      );

      setStockData(formattedData);
      setName(res.data.company);
    } catch (error) {
      console.error('Có lỗi xảy ra khi truy cập dữ liệu:', error);
    }
  };

  // Gọi API lần đầu khi component mount
  useEffect(() => {
    fetchStockTracking();

    // Thiết lập cập nhật định kỳ (ví dụ: mỗi 1 phút)
    const interval = setInterval(() => {
      fetchStockTracking(); // Gọi API để lấy dữ liệu mới
    }, 60000); // 60000ms = 1 phút

    // Xóa interval khi component unmount
    return () => clearInterval(interval);
  }, []);  // Chỉ gọi khi component mount

  const [options, setOptions] = useState({
    data: getData(),
    title: { text: `${name} .Inc` }, // Hiển thị tên công ty
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

  // // Cập nhật options khi stockData thay đổi
  // useEffect(() => {
  //   setOptions((prevOptions) => ({
  //     ...prevOptions,
  //     data: getData,  // Cập nhật dữ liệu mới vào options
  //   }));
  // }, []);

  // Cập nhật options khi theme thay đổi
  useEffect(() => {
    setOptions((prevOptions) => ({
      ...prevOptions,
      theme: 'ag-sheets',
    }));
  }, [theme.palette.mode]);

  return <AgFinancialCharts options={options} />;
};

export default StockAgChart;
