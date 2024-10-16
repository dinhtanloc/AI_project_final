import React, { useState, useEffect } from "react";
import { CssBaseline, ThemeProvider } from "@mui/material";
import { ColorModeContext, useMode } from "@theme";
import Layout from "@admin/components/Layout/Layout";

const AdminPage = () => {
  const [theme, colorMode] = useMode();


  return (
    <ColorModeContext.Provider value={colorMode}>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <Layout/>
        
      </ThemeProvider>
    </ColorModeContext.Provider>
  );
}

export default AdminPage;
