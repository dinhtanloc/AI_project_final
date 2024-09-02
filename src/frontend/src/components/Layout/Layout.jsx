import "@styles/page.css"
import { useEffect, useState, Fragment } from "react";
import { useMode } from "@theme";

import Routers from "@routers/Router";
import Topbar from "../global/Topbar"
import ProSlidebar from "../global/ProSidebar"
import useAxios from "@utils/useAxios";

const Layout =() =>{
    const [theme, colorMode] = useMode();
    const [isSidebar, setIsSidebar] = useState(true);


    return(
        <Fragment>
        <div className="app">
          <ProSlidebar isSidebar={isSidebar}  data={staffInfo} />
          <main className="content">
            <Topbar setIsSidebar={setIsSidebar} />
            <Routers/>
          </main>
        </div>
        </Fragment>
    )

}

export default Layout