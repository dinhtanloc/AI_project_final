import { useState, useEffect} from "react";
import { Routes, Route, Navigate, useLocation } from "react-router-dom";
// import Dashboard from "@client/pages/Dashboardpage";
import HomePage from "@client/pages/HomePage";
import LoadingPage from "@client/components/UI/LoadingPage";
import Login from "@client/pages/Login";
import Market from "@client/pages/Market";
import BlogDetails from "@client/pages/BlogDetails";
import Blog from "@client/pages/Blog";
import About from "@client/pages/About";
import MainLayout from "@client/components/UI/MainLayout";
import RadarChart from "@client/components/UI/RadarChart";
import BollingerStock from "@client/components/UI/BollingerStock";
import Contact from "@client/pages/Contact";
import TableComponent from "@client/components/UI/TableComponent"
import ChatbotPage from "@client/pages/ChatbotPage"
// import PredictionDashboard from '@client/pages/PredictionDashboard'
// import Chatbot from '@client/components/UI/Chatbot'
import PrivateRoute from '@utils/PrivateRoute'
import useAxios from "@utils/useAxios";
import StockDashboard from "@client/pages/StockDashboard";
// import Market from "@pages/" 

const Routers = () => {
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
  

  return (
    <Routes>
     
        <Route element={<MainLayout />}>


          <Route path="/" element={<Navigate to="/home" />} />
          <Route path="/home" element={<HomePage />} />
          <Route path="/register" element={<Login />} />
          <Route path="/login" element={<Login />} />
          <Route path="/blogs" element={<Blog />} />
          <Route path="/blogs/:slug" element={<BlogDetails />} />
          <Route path="/about" element={<About />} />
          <Route path="/rada" element={<RadarChart />} />
          <Route path="/stock-market" element={<Market /> } />
          <Route path="/bollinger" element={<BollingerStock />} />
          <Route path="/table" element={<TableComponent />} />
          <Route path="/contact" element={<Contact />} />
          <Route path="/stock-dashboard" element={
            
              <StockDashboard />
            
            // <StockDashboard />
            } />
     
          <Route exact path='/chatbot/' element={<PrivateRoute/>}>
            <Route exact path='/chatbot/'element={<ChatbotPage />}/>
          </Route>
          
        </Route>
    </Routes>
  );
};

export default Routers;
