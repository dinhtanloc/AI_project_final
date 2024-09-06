import React, { useState } from "react";
import { createRoot } from "react-dom/client";
import { AgFinancialCharts } from "ag-charts-react";
import { AgCharts as AgChartsEnterprise } from "ag-charts-enterprise";

AgChartsEnterprise.setLicenseKey(import.meta.env.VITE_AG_CHART);
import "ag-charts-enterprise";
import getData from "@assets/data/stockData"
// import { AgFinancialChartOptions } from "ag-charts-enterprise";

const StockAgChart = () => {
  const [options, setOptions] = useState({
    data: getData(),
    title: { text: "Acme Inc." },
    theme:'ag-financial-dark',
    // width:"950px",
    height:425,
    initialState: {
      annotations: [
        {
          type: "parallel-channel",
          start: {
            x: { __type: "date", value: new Date("2023-10-23").getTime() },
            y: 148.0,
          },
          end: {
            x: { __type: "date", value: new Date("2024-04-12").getTime() },
            y: 207.0,
          },
          height: 14,
        },
        {
          type: "horizontal-line",
          value: 111.0,
          stroke: "#089981",
          axisLabel: {
            fill: "#089981",
          },
        },
        {
          type: "horizontal-line",
          value: 125.0,
          stroke: "#089981",
          axisLabel: {
            fill: "#089981",
          },
        },
        {
          type: "horizontal-line",
          value: 143.8,
          stroke: "#F23645",
          axisLabel: {
            fill: "#F23645",
          },
        },
        {
          type: "horizontal-line",
          value: 200.8,
          stroke: "#F23645",
          axisLabel: {
            fill: "#F23645",
          },
        },
        {
          type: "text",
          text: "Distribution",
          x: {
            __type: "date",
            value: "Thu Feb 22 2024 00:00:00 GMT+0000 (Greenwich Mean Time)",
          },
          y: 207.0103092783505,
        },
        {
          type: "comment",
          text: "Accumulation",
          x: {
            __type: "date",
            value: "Thu Nov 09 2023 00:00:00 GMT+0000 (Greenwich Mean Time)",
          },
          y: 131.7479612248038,
        },
        {
          type: "callout",
          color: "#040404",
          fill: "#6baaf3",
          fillOpacity: 0.6,
          stroke: "#2395ff",
          strokeOpacity: 1,
          strokeWidth: 2,
          text: "Markup",
          start: {
            x: {
              __type: "date",
              value: "Tue Dec 26 2023 00:00:00 GMT+0000 (Greenwich Mean Time)",
            },
            y: 173.2989690721649,
          },
          end: {
            x: {
              __type: "date",
              value: "Tue Jul 25 2023 01:00:00 GMT+0100 (British Summer Time)",
            },
            y: 167.11340206185565,
          },
        },
      ],
    },
  });

  return <AgFinancialCharts options={options} />;
};

export default StockAgChart
