import { useState, useEffect} from "react";
import { Routes, Route, Navigate, useLocation } from "react-router-dom";
import Dashboard from "@admin/pages/Dashboardpage";
import LoadingPage from "@admin/components/UI/LoadingPage";
import PredictionDashboard from '@admin/pages/PredictionDashboard'
// import Chatbot from '@admin/components/UI/Chatbot'
import PrivateRoute from '@utils/PrivateRoute'
// import ChatbotContextProvider from '@admin/context/ChatbotContext.jsx'
import useAxios from "@utils/useAxios";
// import StockMarket from "@pages/" 
const Routers = () => {
  const [isLoading, setIsLoading] = useState(false);
  const [currentUser, setCurrentUser]=useState(false)
  const isUser = useAxios();
  useEffect(() => {
    fetchUser();
  }, []);

  
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
  

  return (
    <Routes>

          <Route path='/dashboard/*' element={<PrivateRoute/>}>
            <Route path="" element={<Dashboard />} />
            <Route path="prediction" element={<PredictionDashboard />} />
            {/* <Route path="chatbot" element={
              <ChatbotContextProvider>
                <Chatbot />
              </ChatbotContextProvider>
              } /> */}
          </Route>
      </Routes>
     
  );
};

export default Routers;
