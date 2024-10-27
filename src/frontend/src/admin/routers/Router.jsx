import { useState, useEffect} from "react";
import { Routes, Route, useLocation } from "react-router-dom";
import Dashboard from "@admin/pages/Dashboardpage";
import LoadingPage from "@admin/components/UI/LoadingPage";
import PredictionDashboard from '@admin/pages/PredictionDashboard'
import PrivateRoute from '@utils/PrivateRoute'
import ChatbotStatistic from '@admin/pages/ChatbotStatistic'
const Routers = () => {
  const [isLoading, setIsLoading] = useState(false);
 
  
  const location = useLocation();

  useEffect(() => {
    setIsLoading(true);

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

          <Route path='admin/*' element={<PrivateRoute/>}>
            <Route path="" element={<Dashboard />} />
            <Route path="prediction" element={<PredictionDashboard />} />
            <Route path="chatbot-statistic" element={<ChatbotStatistic />} />
            {/* <Route path="chatbot-statistic" element={
             
              } /> */}
          </Route>
          
    </Routes>
    
     
  );
};

export default Routers;
