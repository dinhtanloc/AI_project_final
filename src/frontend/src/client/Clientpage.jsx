import React, { useState, useEffect } from "react";
import { CssBaseline, ThemeProvider } from "@mui/material";
import { ColorModeContext, useMode } from "@theme";
import Layout from "@client/components/Layout/Layout"
import { Helmet, HelmetProvider  } from "react-helmet-async";
import ChatbotContextProvider from '@context/ChatbotContext.jsx'
import StockContext from "@context/StockContext";
import ThemeContext from "@context/ThemeContext";
// import 'rsuite/dist/rsuite.css';

const Clientpage = () => {
  const [theme, colorMode] = useMode();
  const [isSidebar, setIsSidebar] = useState(true);
  const [darkMode, setDarkMode] = useState(false);
  const [stockSymbol, setStockSymbol] = useState("ABC");


  return (
    <HelmetProvider>
    <ColorModeContext.Provider value={colorMode}>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <ChatbotContextProvider>
          <ThemeContext.Provider value={{ darkMode, setDarkMode }}>
            <StockContext.Provider value={{ stockSymbol, setStockSymbol }}>
              <Layout/>
            </StockContext.Provider>
          </ThemeContext.Provider>
        </ChatbotContextProvider>
        
      </ThemeProvider>
    </ColorModeContext.Provider>

    </HelmetProvider>
  );
}

export default Clientpage;
