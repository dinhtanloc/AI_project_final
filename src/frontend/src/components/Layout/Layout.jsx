import React, { Fragment, useState, useContext, useEffect } from "react";
import { useLocation } from "react-router-dom";
import AuthContext from '@context/AuthContext.jsx';
import useAxios from "@utils/useAxios.js";
// import Header from "../Header/Header";
// import Footer from "../Footer/Footer";
import Login from "@pages/Login";
import Routers from "@routers/Routers";
import axios from 'axios';
import backgroundImage from '@public/media/background_login.png'; 
import "@styles/page.css"
import { useMode } from "@theme";
import Topbar from "../global/Topbar"
import ProSidebar from "../global/ProSidebar"
import HomePage from "@pages/HomePage"
axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';
axios.defaults.withCredentials = true;

const Layout = () => {
  const [theme, colorMode] = useMode();
  const [isSidebar, setIsSidebar] = useState(true);
  const location = useLocation();
  const { logined } = useContext(AuthContext);
  const [currentUser, setCurrentUser] = useState(null);
  // const [searchTerm, setSearchTerm] = useState("");
  const staffInfo={data:{profile:{full_name:'Mi mi', image:'abc.png'}}}
  const api = useAxios();

  useEffect(() => {
    const fetchUser = async () => {
      try {
        const res = await api.get("accounts/test/");
        setCurrentUser(true);
      } catch (error) {
        setCurrentUser(false);
        console.error('Có lỗi xảy ra khi truy cập dữ liệu:', error);
      }
    };
    fetchUser();
  }, []);

  // const handleSearch = (term) => {
  //   setSearchTerm(term);
  // };

  const isLoginPage = location.pathname === "/login" || location.pathname === "/register";
  const isHomePage = location.pathname === "/home";


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
        isHomePage ? (
          <HomePage/>
            
      ) : (
        <Fragment>
          <div className="app">
            <ProSidebar isSidebar={isSidebar}  data={staffInfo} />
            <main className="content">
              <Topbar setIsSidebar={setIsSidebar} />
              <Routers/>
            </main>
          </div>
        </Fragment>

      )
      )}
    </>
  );
};

export default Layout;
