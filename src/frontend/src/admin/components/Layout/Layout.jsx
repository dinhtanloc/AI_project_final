import "@admin/styles/page.css"
import { useEffect, useState, Fragment } from "react";
import { useMode } from "@theme";

import Routers from "@admin/routers/Router";
import Topbar from "../global/Topbar"
import ProSidebar from "../global/ProSidebar"
import useAxios from "@utils/useAxios";

const Layout =() =>{
    const [theme, colorMode] = useMode();
    const [isSidebar, setIsSidebar] = useState(true);
    const isStaff = useAxios() 
    const [checkedStaff, checkStaff ] = useState(false)
    const [staffInfo, ListstaffInfo] = useState([])



    useEffect(() => {
      fetchStaffChecking();

    }, []);

    const fetchStaffChecking = async () => {
        try {
            const response = await isStaff.get('accounts/user/staff/');
            checkStaff(response.data.is_staff);
            ListstaffInfo(response.data.staff)
            
        } catch (error) {
            console.error('Error fetching user profile:', error);
        }
    };
    
    
    if(!checkedStaff){
      return(<div>You can not access here</div>);
    }
    return(
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

}

export default Layout