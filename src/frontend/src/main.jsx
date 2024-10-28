import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'

import "bootstrap/dist/css/bootstrap.min.css";
import "remixicon/fonts/remixicon.css";
import "slick-carousel/slick/slick.css";
import "slick-carousel/slick/slick-theme.css";
import App from './App.jsx'
import reportWebVitals from './reportWebVitals.jsx';
import './index.css'
console.warn = () => {};
console.error = () => {};
const onPerfEntry = (metric) => {
  console.log(metric); 
};




createRoot(document.getElementById('root')).render(
   <StrictMode>
     <App />
   </StrictMode>,

)

reportWebVitals(onPerfEntry);