import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import {NextUIProvider} from '@nextui-org/react'
import { BrowserRouter as Router } from "react-router-dom";
import { AuthProvider } from '@context/AuthContext.jsx';
import { AuthLoginProvider } from '@context/AuthLoginContext.jsx';
import "bootstrap/dist/css/bootstrap.min.css";
// import 'swiper/swiper-bundle.min.css';
import "remixicon/fonts/remixicon.css";
import "slick-carousel/slick/slick.css";
import "slick-carousel/slick/slick-theme.css";
// import App from './App.jsx'
import Clientpage from '@client/Clientpage.jsx';
import AdminPage from '@admin/AdminPage.jsx'
import { Provider } from "@context/dataContext";

import './index.css'
// console.log(import.meta.env.VITE_AG_CHART)
// console.warn = () => {};  // Tắt cảnh báo
// console.error = () => {}; // Tắt lỗi

const url = window.location.pathname;

if (url.startsWith('/admin')) {
  createRoot(document.getElementById('root')).render(
    <StrictMode>
    <Router>
      <AuthProvider>
        <AuthLoginProvider>
            <NextUIProvider>
                <Provider>
                  <AdminPage />

                </Provider>

            </NextUIProvider>

          
          </AuthLoginProvider>

      </AuthProvider>

    </Router>
  </StrictMode>

  )

}
else{

createRoot(document.getElementById('root')).render(
  // <StrictMode>
  //   <App />
  // </StrictMode>,
  <StrictMode>
    <Router>
      <AuthProvider>
        <AuthLoginProvider>
            <NextUIProvider>
                <Provider>
                  <Clientpage />

                </Provider>

            </NextUIProvider>

          
          </AuthLoginProvider>

      </AuthProvider>

    </Router>
  </StrictMode>
)
}
