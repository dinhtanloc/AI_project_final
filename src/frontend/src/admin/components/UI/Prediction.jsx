import React from "react";
import useData from "@context/dataContext";
import { Typography, Box } from "@mui/material";
import { useTheme } from "@mui/material";
import { tokens } from "@theme";
export default function Prediction() {
  const { price } = useData(); 
  const theme = useTheme();
  const colors = tokens(theme.palette.mode);

  var predprice = Number(price[0]).toFixed(2);  

  return (
    <Box>
      <Typography
        variant="h3"
        sx={{
          pt: 5,
          pb: 4,
          fontFamily: "Roboto Flex",
          color: colors.lightPred[500], 
          fontSize: { lg: 45, md: 45, sm: 35, xs: 25 },  
        }}
      >
        Price Prediction
      </Typography>
      <Box
        sx={{
          bgcolor: colors.lightPred[700],  
          width: { lg: "200px", md: "200px", sm: "150px" },  
          borderRadius: "10px",  
          p: 2,
          textAlign: "center",  
          fontSize: { lg: 25, md: 25, sm: 18, xs: 17 },  
          boxShadow: `0px 0px 15px ${colors.lightPred[1800]}`,  
        }}
      >
        {predprice}
      </Box>
    </Box>
  );
}
