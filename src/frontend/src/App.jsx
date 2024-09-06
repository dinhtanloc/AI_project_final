import React, { useState, useEffect } from "react";
import { CssBaseline, ThemeProvider } from "@mui/material";
import { ColorModeContext, useMode } from "@theme";
import Layout from "@components/Layout/Layout"
import { Helmet, HelmetProvider  } from "react-helmet-async";

const App = () => {
  const [theme, colorMode] = useMode();
  const [isSidebar, setIsSidebar] = useState(true);


  return (
    <HelmetProvider>
    <ColorModeContext.Provider value={colorMode}>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <Layout/>
        
      </ThemeProvider>
    </ColorModeContext.Provider>

    </HelmetProvider>
  );
}

export default App;
