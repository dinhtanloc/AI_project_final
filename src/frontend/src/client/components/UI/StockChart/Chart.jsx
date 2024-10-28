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

import ThemeContext from "@context/ThemeContext";
import StockContext from "@context/StockContext";
import {
  createDate,
} from "@utils/date-helper";
import { chartConfig } from "@constants/config";
import useAxios from '@utils/useAxios';
import { useNavigate } from "react-router-dom"; 



const Chart = () => {
  const [filter, setFilter] = useState("1W");
  const navigate = useNavigate()
  const { darkMode } = useContext(ThemeContext);

  const { stockSymbol } = useContext(StockContext);

  const [data, setData] = useState([]);
  const stock=useAxios();

  const formatData = (data, resolution) => {
    return data.map((item) => {
      const date = new Date(item.date); 
  
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
        date: formattedDate, 
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
  
      
    
      return startDate
    };
    const startTimestampUnix  = getDateRange();
    const resolution = chartConfig[filter].resolution;
    const updateChartData = async () => {
      try {
      
        const response = await stock.get(`/prediction/predict/?start=${startTimestampUnix}&symbol=${stockSymbol}&interval=${resolution}`);
        if(response.status === 200){
                      Swal.fire({
                          title: "Prediction Successful",
                          icon: "success",
                          toast: true,
                          timer: 2000,
                          position: 'top-right',
                          timerProgressBar: true,
                          showConfirmButton: false,
                      })
          
                  } else {    
                      Swal.fire({
                          title: "Outdated model! Admin need to train model",
                          icon: "error",
                          toast: true,
                          timer: 2000,
                          position: 'top-right',
                          timerProgressBar: true,
                          showConfirmButton: false,
                      })
                  }
              
        setData(formatData(response.data.data,resolution));
      
      } catch (error) {
        console.log(error);
      }
    };


    updateChartData();
    const intervalId = setInterval(updateChartData, 60000);

    return () => clearInterval(intervalId);
  }, [filter]);



//   import Swal from "sweetalert2";



// const AuthContext = createContext();

// export default AuthContext

// export const AuthProvider = ({ children }) => {
//     const navigate =useNavigate()
//     const [logined, isLogin] = useState(null)
//     const [authTokens, setAuthTokens] = useState(() =>
//         localStorage.getItem("authTokens")
//             ? JSON.parse(localStorage.getItem("authTokens"))
//             : null
//     );
    

//     const [user, setUser] = useState(() => 
//         localStorage.getItem("authTokens")
//             ? jwtDecode (localStorage.getItem("authTokens"))
//             : null
//     );


//     const [loading, setLoading] = useState(true);

//     // const navigate = useNavigate();

//     const loginUser = async (email, password) => {
//         const response = await fetch("http://127.0.0.1:8000/accounts/token/", {
//             method: "POST",
//             headers:{
//                 "Content-Type":"application/json"
//             },
//             body: JSON.stringify({
//                 email, password
//             })
//         })
//         const data = await response.json()

//         if(response.status === 200){
//             setAuthTokens(data)
//             setUser(jwtDecode (data.access))
//             localStorage.setItem("authTokens", JSON.stringify(data))
//             isLogin(true);
//             navigate("/") // chuyen trang
//             Swal.fire({
//                 title: "Login Successful",
//                 icon: "success",
//                 toast: true,
//                 timer: 2000,
//                 position: 'top-right',
//                 timerProgressBar: true,
//                 showConfirmButton: false,
//             })

//         } else {    
//             Swal.fire({
//                 title: "Username or passowrd does not exists",
//                 icon: "error",
//                 toast: true,
//                 timer: 2000,
//                 position: 'top-right',
//                 timerProgressBar: true,
//                 showConfirmButton: false,
//             })
//         }
//     }


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
            <linearGradient id="StockColor" x1="0" y1="0" x2="0" y2="1">
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
            <linearGradient id="PredictColor" x1="0" y1="0" x2="0" y2="1">
              <stop
                offset="5%"
                stopColor={darkMode ? "#b52b37" : "#1897c9"}
                stopOpacity={0.8}
              />
              <stop
                offset="95%"
                stopColor={darkMode ? "#b52b37" : "#1897c9"}
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
            fill="url(#StockColor)"
            fillOpacity={1}
            strokeWidth={0.5}
          />
          <Area
            type="monotone"
            dataKey="predict_value"  
            stroke="#1897c9"
            fill="url(#PredictColor)"
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
