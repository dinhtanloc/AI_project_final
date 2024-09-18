import React, { Fragment, useState, useContext, useEffect } from "react";
import { useLocation } from "react-router-dom";
import AuthContext from '@context/AuthContext.jsx';
import useAxios from "@utils/useAxios.js";
import Login from "@pages/Login";
import Routers from "@routers/Routers";
import axios from 'axios';
import backgroundImage from '/media/background_login.png'; 
import "@styles/page.css"
import Topbar from "../global/Topbar"
import ProSidebar from "../global/ProSidebar"
import Header from "@components/Header/Header";
import Footer from "@components/Footer/Footer"
axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';
axios.defaults.withCredentials = true;

const Layout = () => {
  // const [theme, colorMode] = useMode();
  const [isSidebar, setIsSidebar] = useState(true);
  const location = useLocation();
  const { logined } = useContext(AuthContext);
  const [currentUser, setCurrentUser] = useState(null);
  const [searchTerm, setSearchTerm] = useState("");
  const staffInfo={data:{profile:{full_name:'Mi mi', image:'abc.png'}}}
  const api = useAxios();

  useEffect(() => {
    const fetchUser = async () => {
      try {
        const res = await api.get("accounts/user/current-user/");
        setCurrentUser(true);
      } catch (error) {
        setCurrentUser(false);
        console.error('Có lỗi xảy ra khi truy cập dữ liệu:', error);
      }
    };
    fetchUser();
  }, []);

  const handleSearch = (term) => {
    setSearchTerm(term);
  };

  const isLoginPage = location.pathname === "/login" || location.pathname === "/register";
  // const isDashboard = location.pathname === "/dashboard";
  const isDashboard = location.pathname.startsWith("/dashboard");



  return (
    <>
      {isLoginPage ? (
        <div
          className="login_outside"
          style={{
            width: '100vw',
            height: '100vh',
            background: `linear-gradient(rgba(0, 13, 107, 0.5), rgba(0, 13, 107, 0.5)), url("${backgroundImage}")`,
            backgroundPosition: 'center',
            backgroundRepeat: 'no-repeat',
            backgroundSize: 'cover',
          }}
        >
          <Login />
        </div>
      ) : (
        isDashboard ? (
          <Fragment>
            <div className="app" style={{display:'flex'}}>
              <ProSidebar isSidebar={isSidebar}  data={staffInfo} />
              <main className="content" style={{flex:'1', overflowY:'auto', padding:'20px'}}>
                <Topbar setIsSidebar={setIsSidebar} />
                <Routers IsDashboard ={isDashboard}/>
              </main>
            </div>
          </Fragment>
          // <HomePage/>
            
      ) : (
        <Fragment>
          <Header onSearch={handleSearch} />
          <Routers IsDashboard ={isDashboard} />
          
          {/* <ChatPopup /> */}
          <Footer />
        </Fragment>

      )
      )}
    </>
  );
};

export default Layout;
