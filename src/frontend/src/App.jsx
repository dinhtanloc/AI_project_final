
import React, { useState, useEffect } from "react";
import { BrowserRouter as Router } from "react-router-dom";
import { AuthProvider } from '@context/AuthContext.jsx';
import { AuthLoginProvider } from '@context/AuthLoginContext.jsx';
import {NextUIProvider} from '@nextui-org/react'
import Clientpage from '@client/Clientpage.jsx';
import AdminPage from '@admin/AdminPage.jsx'
import { Provider } from "@context/dataContext";
// import 'rsuite/dist/rsuite.css';

const App = () => {
    console.log('ok')
  const url = window.location.pathname;
  if (url.startsWith('/admin')) {
    return(

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
    );

  } else{
    return(

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
);
  }
}
export default App;
