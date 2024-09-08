import { useState, useEffect, Fragment } from "react";
import { Routes, Route, Navigate, useLocation } from "react-router-dom";
import Dashboard from "@pages/Dashboardpage";
import HomePage from "@pages/HomePage";
import LoadingPage from "@components/UI/LoadingPage";
import Login from "@pages/Login";
import StockMarket from "@pages/StockMarket";
import BlogDetails from "@pages/BlogDetails";
import Blog from "@pages/Blog";
import About from "@pages/About";
import MainLayout from "@components/UI/MainLayout";
import RadarChart from "@components/UI/RadarChart";
import BollingerStock from "@components/UI/BollingerStock";
import CandleStickChartWithBollingerBandOverlay from "@components/UI/CandleStickChartWithBollingerBandOverlay";
import getData from "@assets/data/stockData"
import TableComponent from "@components/UI/TableComponent"
// import StockMarket from "@pages/" 
const Routers = ({ IsDashboard }) => {
  const [isLoading, setIsLoading] = useState(true);
  const location = useLocation();

  useEffect(() => {
    setIsLoading(true);

    const timer = setTimeout(() => {
      setIsLoading(false);
    }, 1000); // Giả lập thời gian tải trang

    return () => clearTimeout(timer);
  }, [location]);

  if (isLoading) {
    return <LoadingPage />;
  }
  
  console.log(IsDashboard);

  return (
    <Routes>
      {IsDashboard ? (
        <>
          <Route path="/dashboard" element={<Dashboard />} />
          {/* <Route path="/dashboard/abc" element={<Login />} /> */}
          {/* <Route path="/login" element={<Login />} /> */}
        </>
      ) : (
        <Route element={<MainLayout />}>
          <Route path="/" element={<Navigate to="/home" />} />
          <Route path="/home" element={<HomePage />} />
          {/* <Route path="/dashboard" element={<Dashboard />} /> */}
          <Route path="/register" element={<Login />} />
          <Route path="/login" element={<Login />} />
          <Route path="/blogs" element={<Blog />} />
          <Route path="/blogs/:slug" element={<BlogDetails />} />
          <Route path="/about" element={<About />} />
          <Route path="/rada" element={<RadarChart />} />
          <Route path="/stock-market" element={<StockMarket />} />
          <Route path="/bollinger" element={<BollingerStock />} />
          <Route path="/candle" element={<CandleStickChartWithBollingerBandOverlay data={getData()} width={850} ratio={1} />} />
          <Route path="/table" element={<TableComponent />} />
          {/* <Route path="/candle" element={<CandleStickChartWithBollingerBandOverlay data={getData()} width={850} ratio={1} />} /> */}
        </Route>
      )}
    </Routes>
  );
};

export default Routers;
