import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import {NextUIProvider} from '@nextui-org/react'
import { BrowserRouter as Router } from "react-router-dom";
import { AuthProvider } from './context/AuthContext.jsx';
import { AuthLoginProvider } from './context/AuthLoginContext.jsx';
import "bootstrap/dist/css/bootstrap.min.css";
// import 'swiper/swiper-bundle.min.css';
import "remixicon/fonts/remixicon.css";
import "slick-carousel/slick/slick.css";
import "slick-carousel/slick/slick-theme.css";
import App from './App.jsx'
import './index.css'

createRoot(document.getElementById('root')).render(
  // <StrictMode>
  //   <App />
  // </StrictMode>,
  <StrictMode>
    <Router>
      <AuthProvider>
        <AuthLoginProvider>
            <NextUIProvider>

              <App />
            </NextUIProvider>

          
          </AuthLoginProvider>

      </AuthProvider>

    </Router>
  </StrictMode>
)
