import { useState, useEffect} from "react";
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
import Contact from "@pages/Contact";
import TableComponent from "@components/UI/TableComponent"
import PredictionDashboard from '@pages/PredictionDashboard'
import Chatbot from '@components/UI/Chatbot'
import PrivateRoute from '@utils/PrivateRoute'
import ChatbotContextProvider from '@context/ChatbotContext.jsx'
import useAxios from "@utils/useAxios";
// import StockMarket from "@pages/" 
const Routers = ({ IsDashboard }) => {
  const [isLoading, setIsLoading] = useState(false);
  const [currentUser, setCurrentUser]=useState(false)
  const isUser = useAxios();
  useEffect(() => {
    fetchUser();
  }, []);

  const fetchUser = async () => {
      try {
          const response = await isUser.get('accounts/user/current-user');
          response ? setCurrentUser(true) : null;          
      } catch (error) {
          setCurrentUser(false);
          console.error('Error fetching user profile:', error);
      }
  };
  const location = useLocation();

  useEffect(() => {
    if(currentUser){
      setIsLoading(true);

    }

    const timer = setTimeout(() => {
      setIsLoading(false);
    }, 1000); 

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
          {/* <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/dashboard/prediction" element={<PredictionDashboard />} />
          <Route path="/dashboard/chatbot" element={
            <ChatbotContextProvider>
              <Chatbot />
            </ChatbotContextProvider>
            } /> */}
          <Route path='/dashboard/*' element={<PrivateRoute/>}>
            <Route path="" element={<Dashboard />} />
            <Route path="prediction" element={<PredictionDashboard />} />
            <Route path="chatbot" element={
              <ChatbotContextProvider>
                <Chatbot />
              </ChatbotContextProvider>
              } />
          </Route>
            {/* <Route exact path='/dashboard/*' element={<Profile/>}/> */}
          {/* <Route exact path='/dashboard/' element={<PrivateRoute/>}> */}
          {/* </Route> */}
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
          {/* <Route path="/candle" element={<CandleStickChartWithBollingerBandOverlay data={getData()} width={800} ratio={8} />} /> */}
          <Route path="/table" element={<TableComponent />} />
          <Route path="/contact" element={<Contact />} />
          <Route path="/prediction" element={<PredictionDashboard />} />
          {/* <Route path="/candle" element={<CandleStickChartWithBollingerBandOverlay data={getData()} width={850} ratio={1} />} /> */}
        </Route>
      )}
    </Routes>
  );
};

export default Routers;
