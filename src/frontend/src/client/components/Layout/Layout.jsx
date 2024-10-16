import React, { Fragment, useState, useContext, useEffect } from "react";
import { useLocation } from "react-router-dom";
import AuthContext from '@context/AuthContext.jsx';
import useAxios from "@utils/useAxios.js";
import Login from "@client/pages/Login";
import Routers from "@client/routers/Routers";
import axios from 'axios';
import backgroundImage from '/media/background_login.png'; 
import "@client/styles/page.css"
// import Topbar from "../global/Topbar"
// import ProSidebar from "../global/ProSidebar"
import Header from "@client/components/Header/Header";
import Footer from "@client/components/Footer/Footer"
axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';
axios.defaults.withCredentials = true;

const Layout = () => {
  // const [theme, colorMode] = useMode();
  const [isSidebar, setIsSidebar] = useState(true);
  const location = useLocation();
  const { logined } = useContext(AuthContext);
  const[name,setName]=useState('');
  const[img,setImage]=useState('');
  const [currentUser, setCurrentUser] = useState(null);
  const [searchTerm, setSearchTerm] = useState("");
  const api = useAxios();

  useEffect(() => {
    const fetchUser = async () => {
      try {
        const res = await api.get("accounts/user/current-user/");
        setCurrentUser(true);
        const name_login = res.data.response.username;
        setName(name_login)
      } catch (error) {
        setCurrentUser(false);
        console.error('Có lỗi xảy ra khi truy cập dữ liệu:', error);

      }
    };

    const fetchProfile = async () => {
      try {
        const res = await api.get("accounts/user/profile/");
        setCurrentUser(true);
        const profile = res.data;
        var imgUrl = profile.image
        setImage(imgUrl)
        // setName(profile)
      } catch (error) {
        setCurrentUser(false);
        console.error('Có lỗi xảy ra khi truy cập dữ liệu:', error);

      }
    };

    // const fetchStaffChecking = async () => {
    //   try {
    //       const response = await api.get('accounts/user/staff/');
    //       // setUserProfile(response.data);
    //       checkStaff(response.data.is_staff);
          
    //   } catch (error) {
    //       console.error('Error fetching user profile:', error);
    //   }
  // };

    fetchUser();
    fetchProfile();
    // fetchStaffChecking();
  }, []);

  const handleSearch = (term) => {
    setSearchTerm(term);
  };

  const isLoginPage = location.pathname === "/login" || location.pathname === "/register";
  // const isDashboard = location.pathname === "/dashboard";
  // const isDashboard = location.pathname.startsWith("/dashboard");



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

        <Fragment>
          <Header onSearch={handleSearch} />
          <Routers/>
          
          {/* <ChatPopup /> */}
          <Footer />
        </Fragment>

      
      )}
    </>
  );
};

export default Layout;
