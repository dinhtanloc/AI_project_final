import { useState, useEffect } from "react";
import { Routes, Route, Navigate, useLocation } from "react-router-dom";
import Dashboard from "@pages/Dashboardpage";
import HomePage from "@pages/HomePage";
import LoadingPage from "@components/UI/LoadingPage";
import Login from "@pages/Login"
const Routers = ({IsDashboard}) => {
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
  console.log(IsDashboard)
  return (
    <Routes>
      {IsDashboard ? (
        <>
          <Route path="/dashboard" element={<Dashboard />} />
          {/* <Route path="/dashboard/abc" element={<Login />} /> */}
          {/* <Route path="/login" element={<Login />} /> */}
        </>
      ) : (
        <>
          <Route path="/" element={<Navigate to="/home" />} />
          <Route path="/home" element={<HomePage />} />
          {/* <Route path="/dashboard" element={<Dashboard />} /> */}
          <Route path="/register" element={<Login />} />
          <Route path="/login" element={<Login />} />
        </>
      )}
    </Routes>
  );
  };
  
  export default Routers;