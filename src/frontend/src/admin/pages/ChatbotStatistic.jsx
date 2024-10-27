import { Box, Button, useTheme } from "@mui/material";
import { tokens } from "@theme";
import DownloadOutlinedIcon from "@mui/icons-material/DownloadOutlined";
import Header from "./HeaderDashboard";
import ChatbotAdmin from '@admin/components/UI/ChatbotAdmin'
import ChatbotContextProvider from '@context/ChatbotContext.jsx'

const ChatbotStatistic = () => {



  // window.location.reload()
  const theme = useTheme();
  const colors = tokens(theme.palette.mode);


  
  
  const handleRedirect = () => {
    window.location.href = import.meta.env.VITE_LANGSMITH;
  };

  


 
  
  return (
    <Box m="20px">
      {/* HEADER */}
      <Box display="flex" justifyContent="space-between" alignItems="center">
        <Header title="" subtitle="" />
        <Box>
          <Button
            sx={{
              backgroundColor: colors.blueAccent[700],
              color: colors.grey[100],
              fontSize: "14px",
              fontWeight: "bold",
              padding: "10px 20px",
            }}
            onClick = {handleRedirect}
          >
            <DownloadOutlinedIcon sx={{ mr: "10px" }} />
            Performance
          </Button>
        </Box>
      </Box>

      <ChatbotContextProvider>
        <ChatbotAdmin />
      </ChatbotContextProvider>

    </Box>
  );
};

export default ChatbotStatistic;
