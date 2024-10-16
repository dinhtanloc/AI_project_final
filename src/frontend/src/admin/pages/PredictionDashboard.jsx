import React from "react";
import useData from "@context/dataContext";
import { Box, Typography } from "@mui/material";
import DateStockePicker from "@admin/components/UI/DateStockePicker";
import ModelPerformance from "@admin/components/UI/ModelPerformance";
import { DotLoader } from "react-spinners";
import '@admin/styles/predictions.css';
import QuoteLIneChart from '@admin/components/UI/QuoteLIneChart';
import { useTheme } from "@mui/material";
import { tokens } from "@theme";
export default function PredictionDashboard() {
  const theme = useTheme();
  const colors = tokens(theme.palette.mode);
  console.log(colors.lightPred[100])

  const { priceHistory, parseData, loading } = useData();
  // console.log(priceHistory)
  // console.log(loading)
  return (
    <div className="prediction-main">

    <Box
      sx={{
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
        alignItems: "center",
        pt: 5,
      }}
    >
      <DateStockePicker />
      {priceHistory.length === 0 && loading === false ? (
        <Typography
          variant="h5"
          sx={{
            mt: 10,
            // color: "rgba(88, 95, 138, 1)",
            color: colors.lightPred[100],
            fontSize: { lg: 40, md: 35, sm: 20, xs: 15 },
          }}
        >
          Select a start/end date and stock to train your model.
        </Typography>
      ) : loading === true ? (
        <Box
          sx={{
            mt: 10,
            display: "flex",
            flexDirection: "column",
            justifyContent: "center",
            alignItems: "center",
          }}
        >
          <DotLoader color={colors.lightPred[300]} size={150} />
          {/* <Typography sx={{ color: colors.grey[100], mt: 3 }}> */}
          <Typography sx={{ color: "#03FFF9", mt: 3 }}>
            Model in training
          </Typography>
        </Box>
      ) : (
        <QuoteLIneChart />
      )}

      {loading === true ? null : parseData.length !== 0 ? (
        <ModelPerformance />
      ) : null}
    </Box>
    </div>
  );
}
