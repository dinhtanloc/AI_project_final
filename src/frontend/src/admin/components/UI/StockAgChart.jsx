import React, { useState, useEffect } from "react";
import { useTheme } from "@mui/material";
import { createRoot } from "react-dom/client";
import { AgFinancialCharts } from "ag-charts-react";
import { AgCharts as AgChartsEnterprise } from "ag-charts-enterprise";
import { tokens } from "@theme";

AgChartsEnterprise.setLicenseKey(import.meta.env.VITE_AG_CHART);
import "ag-charts-enterprise";
import getData from "@assets/data/stockData"
// import { AgFinancialChartOptions } from "ag-charts-enterprise";
const StockAgChart = () => {
  const theme = useTheme();

  const [options, setOptions] = useState({
    data: getData(),
    title: { text: "VIC Inc." },
    theme: theme.agCharts.theme,
    navigator: true,
    toolbar: true,
    rangeButtons: true,
    volume: true,
    statusBar: true,
    zoom: true,
    width: 1200,
    height: 420,
  });

  // useEffect để cập nhật `options` khi `theme.palette.mode` thay đổi
  useEffect(() => {
    setOptions((prevOptions) => ({
      ...prevOptions,
      theme: theme.agCharts.theme,
    }));
  }, [theme.palette.mode]);

  return <AgFinancialCharts options={options} />;
};

export default StockAgChart
