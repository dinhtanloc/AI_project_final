import { useState, useEffect } from "react";
import { Routes, Route, Navigate, useLocation } from "react-router-dom";
import Dashboard from "@pages/Dashboardpage";

const Routers = () => {
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
    return (
      <Routes>
              <Route path="/" element={<Navigate to="/home" />} />
              <Route path="/home" element={<Dashboard />} />
              
      </Routes>
    );
  };
  
  export default Routers;