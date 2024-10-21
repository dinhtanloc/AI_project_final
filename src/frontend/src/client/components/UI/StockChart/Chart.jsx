import React, { useContext, useEffect, useState } from "react";
import ChartFilter from "./ChartFilter";
import Card from "./Card";
import {
  Area,
  XAxis,
  YAxis,
  ResponsiveContainer,
  AreaChart,
  Tooltip,
} from "recharts";
import ChatIcon from '@mui/icons-material/Chat'; // Import icon Chat

import ThemeContext from "@context/ThemeContext";
import StockContext from "@context/StockContext";
import { Box, Button, Typography, Icon } from "@mui/material";
import {
  createDate,
  convertDateToUnixTimestamp,
  convertUnixTimestampToDate,
} from "@utils/date-helper";
import { chartConfig } from "@constants/config";
import useAxios from '@utils/useAxios';
import { useNavigate } from "react-router-dom"; // Điều hướng



const Chart = () => {
  const [filter, setFilter] = useState("1W");
  const navigate = useNavigate()
  const { darkMode } = useContext(ThemeContext);

  const { stockSymbol } = useContext(StockContext);

  const [data, setData] = useState([]);
  const stock=useAxios();

  const formatData = (data, resolution) => {
    // console.log(data);
    return data.map((item) => {
      const date = new Date(item.date); // Chuyển chuỗi thành Date object
  
      // Định dạng ngày theo resolution
      let formattedDate;
      const monthNames = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
  
      switch (resolution) {
        case '1D':
          formattedDate = `${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`;
          break;
        case '1m':
          formattedDate = `${String(date.getHours()).padStart(2, '0')}:${String(date.getMinutes()).padStart(2, '0')}`;
          break;
        case '1W':
          formattedDate = `${monthNames[date.getMonth()]}-${String(date.getDate()).padStart(2, '0')}`;
          break;
        case '1M':
          formattedDate = `${monthNames[date.getMonth()]}-${date.getFullYear()}`;
          break;
        default:
          formattedDate = date.toString();
      }
  
      return {
        ...item,
        date: formattedDate, // Cập nhật trường date với định dạng tương ứng
      };
    });
  };

  useEffect(() => {
    const getDateRange = () => {
      const { days, weeks, months, years } = chartConfig[filter];

      var endDate = new Date();
      const yearendDate = endDate.getFullYear();
      const monthendDate = String(endDate.getMonth() + 1).padStart(2, '0'); // Tháng bắt đầu từ 0
      const dayendDate = String(endDate.getDate()).padStart(2, '0');
      endDate = `${yearendDate}-${monthendDate}-${dayendDate}`;
      
      var startDate = createDate(endDate, -days, -weeks, -months, -years);
      const year = startDate.getFullYear();
      const month = String(startDate.getMonth() + 1).padStart(2, '0'); // Tháng bắt đầu từ 0
      const day = String(startDate.getDate()).padStart(2, '0');
      startDate = `${year}-${month}-${day}`;
      console.log(startDate)
      console.log(endDate)
      console.log(filter)
      
      // const startTimestampUnix = convertDateToUnixTimestamp(startDate);
      // const endTimestampUnix = convertDateToUnixTimestamp(endDate);
      // console.log({ startTimestampUnix, endTimestampUnix });
      return startDate
    };
    
    const fetchStockTracking = async () => {
      try {
        const startTimestampUnix  = getDateRange();
        console.log(startTimestampUnix)
        // console.log(endTimestampUnix)
        const resolution = chartConfig[filter].resolution;
          const res = await stock.post("/stock/stocktracking/historicalclosedata/", {
            start: startTimestampUnix, 
            interval: resolution 
          });
          // const formattedData = res.data.price_data.map(item => {
          //   const date = new Date(item.date); // Chuyển chuỗi thành Date object
      
          //   // Kiểm tra độ phân giải để định dạng ngày
          //   let formattedDate;
          //   if (resolution === '1D') {
          //     // Định dạng 'YYYY-MM-DD' cho 1D
          //     formattedDate = date.toISOString().split('T')[0];
          //   } else if (resolution === '1m') {
          //     // Định dạng 'YYYY-MM-DD HH:mm' cho 1m
          //     formattedDate = date.toISOString().split('T')[0] + ' ' + date.toTimeString().split(' ')[0].slice(0, 5); // Lấy giờ và phút
          //   } else {
          //     // Nếu không có độ phân giải cụ thể, giữ nguyên
          //     formattedDate = date.toISOString();
          //   }
      
          //   return {
          //     ...item,
          //     date: formattedDate // Cập nhật trường date với định dạng tương ứng
          //   };
          // });
          // console.log(formattedData)
          console.log(formatData(res.data.price_data, resolution))
          setData(formatData(res.data.price_data,resolution));
        } catch (error) {
          setData([]);
          console.error('Có lỗi xảy ra khi truy cập dữ liệu:', error);
        }
      };

    const updateChartData = async () => {
      // try {
      //   const { startTimestampUnix, endTimestampUnix } = getDateRange();
      //   const resolution = chartConfig[filter].resolution;
      //   const result = await fetchHistoricalData(
      //     stockSymbol,
      //     resolution,
      //     startTimestampUnix,
      //     endTimestampUnix
      //   );
      //   setData(formatData(result));
      // } catch (error) {
      //   setData([]);
      //   console.log(error);
      // }
    };


    fetchStockTracking();
    updateChartData();
  }, [filter]);

  return (
    <>
    <Card>
      <ul className="flex absolute top-2 right-2 z-40">
        {Object.keys(chartConfig).map((item) => (
          <li key={item}>
            <ChartFilter
              text={item}
              active={filter === item}
              onClick={() => {
                setFilter(item);
              }}
            />
          </li>
        ))}
      </ul>
      <ResponsiveContainer>
        <AreaChart data={data}>
          <defs>
            <linearGradient id="chartColor" x1="0" y1="0" x2="0" y2="1">
              <stop
                offset="5%"
                stopColor={darkMode ? "#312e81" : "rgb(199 210 254)"}
                stopOpacity={0.8}
              />
              <stop
                offset="95%"
                stopColor={darkMode ? "#312e81" : "rgb(199 210 254)"}
                stopOpacity={0}
              />
            </linearGradient>
          </defs>
          <Tooltip
            contentStyle={darkMode ? { backgroundColor: "#111827" } : null}
            itemStyle={darkMode ? { color: "#818cf8" } : null}
          />
          <Area
            type="monotone"
            dataKey="value"
            stroke="#312e81"
            fill="url(#chartColor)"
            fillOpacity={1}
            strokeWidth={0.5}
          />
          <XAxis dataKey="date" />
          <YAxis domain={["dataMin", "dataMax"]} />
        </AreaChart>
      </ResponsiveContainer>
    </Card>
    
    </>
  );
};

export default Chart;
