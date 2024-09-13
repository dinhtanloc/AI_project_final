import React from "react";
import useData from "@context/dataContext";
import { Typography, Box } from "@mui/material";

export default function Prediction() {
  const { price } = useData();  // Retrieving predicted price data from the context

  var predprice = Number(price[0]).toFixed(2);  // Formatting the predicted price to 2 decimal places

  return (
    <Box>
      <Typography
        variant="h3"
        sx={{
          pt: 5,
          pb: 4,
          fontFamily: "Roboto Flex",
          color: "rgba(255,255,255,0.8)",  // Semi-transparent white color
          fontSize: { lg: 45, md: 45, sm: 35, xs: 25 },  // Responsive font sizes
        }}
      >
        Price Prediction
      </Typography>
      <Box
        sx={{
          bgcolor: "rgba(3,255,249,0.8)",  // Light cyan color with some transparency
          width: { lg: "200px", md: "200px", sm: "150px" },  // Responsive width
          borderRadius: "10px",  // Rounded corners
          p: 2,  // Padding
          textAlign: "center",  // Centered text
          fontSize: { lg: 25, md: 25, sm: 18, xs: 17 },  // Responsive font sizes
          boxShadow: "0px 0px 15px #03FFF9",  // Glowing box shadow effect
        }}
      >
        {predprice}
      </Box>
    </Box>
  );
}
