import React from "react";
import {
  Box,
  Typography,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
} from "@mui/material";
import useMeasure from "react-use-measure";
import useData from "@context/dataContext";
import * as d3 from "d3";
import { motion } from "framer-motion";
import {
  format,
  startOfMonth,
  endOfMonth,
  endOfYear,
  eachYearOfInterval,
} from "date-fns";
import Prediction from "./Prediction";
import { useTheme } from "@mui/material";
import { tokens } from "@theme";
export default function ModelPerformance() {
  const {
    timeTrain,
    priceTrain,
    priceClose,
    predictionClose,
    timePrediction,
    parseData,
    rmse,
    price,
  } = useData();
  const theme = useTheme();
  const colors = tokens(theme.palette.mode);


  let trainData = [];

  priceTrain.forEach((value, ind) => {
    let date = new Date(timeTrain[ind]);
    trainData.push({ date, value });
  });
  let rmseValue = rmse[0]?.toFixed(2);


  let tableData = [];

  let [ref, bounds] = useMeasure();
  priceClose.forEach((value, ind) => {
    let date = new Date(format(new Date(timePrediction[ind]), "yyyy-MM-dd"));
    let price = Number(value.toFixed(2));
    let predict = Number(predictionClose[ind].toFixed(2));
    tableData.push({ date, price, predict });
  });

  let height = bounds.height;
  let width = bounds.width;
  let margin = {
    top: 20,
    right: 20,
    bottom: 25,
    left: 30,
  };


  let startDay = startOfMonth(parseData?.[0]?.date);
  let endDay = endOfMonth(parseData?.[parseData.length - 1]?.date);
  let months = eachYearOfInterval({ start: startDay, end: endDay });

  let xScale = d3
    .scaleTime()
    .domain([startDay, endDay])
    .range([margin.left, width - margin.right]);

  let yScale = d3
    .scaleLinear()
    .domain(d3.extent(parseData.map((d) => d.value)))
    .range([height - margin.bottom, margin.top]);

  let line = d3
    .line()
    .x((d) => xScale(d.date))
    .y((d) => yScale(d.value));



  let line2 = d3
    .line()
    .x((d) => xScale(d.date))
    .y((d) => yScale(d.price));

  let line3 = d3
    .line()
    .x((d) => xScale(d.date))
    .y((d) => yScale(d.predict));


  let v = line2(tableData);
  let d = line(trainData);
  let p = line3(tableData);

  return (
    <Box
      sx={{
        mt: 3,
        width: "85%",
        height: "auto",
        display: "flex",
        flexDirection: "column",
        justifyContent: "start",
        alignItems: "start",
        pb: 5,
      }}
    >
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
        {" "}
        Model Performance{" "}
      </Typography>
      <Box
        sx={{ width: "100%", display: "flex", gap: 2, position: "relative" }}
      >
        <Box
          sx={{
            position: "absolute",
            bgcolor: colors.lightPred[500],
            left: "1%",
            bottom: 0,
            p: 0.5,
            borderRadius: "10px",
            color:'white'
          }}
        >
          RMSE: {rmseValue}
        </Box>
        <Box
          sx={{
            position: "absolute",
            bgcolor: colors.lightPred[500],
            left: { lg: "68%", md: "45%", sm: "75%", xs: "75%" },
            top: -63,
            p: 0.2,
            borderRadius: "10px",
          }}
        >
          <Box sx={{ display: "flex", alignItems: "center", gap: 1 }}>
            <div
              style={{ height: "3px", background: colors.lightPred[700], width: "20px" }}
            />
            <Typography sx={{ fontSize: 12, color:'white'}}>Train</Typography>
          </Box>
          <Box sx={{ display: "flex", alignItems: "center", gap: 1 }}>
            <div
              style={{ height: "3px", background: colors.lightPred[800], width: "20px" }}
            />
            <Typography sx={{ fontSize: 12, color:'white' }}>Price</Typography>
          </Box>
          <Box sx={{ display: "flex", alignItems: "center", gap: 1 }}>
            <div
              style={{ height: "3px", background: colors.lightPred[900], width: "20px" }}
            />
            <Typography sx={{ fontSize: 12, color:'white' }}>Prediction</Typography>
          </Box>
        </Box>
        <Box
          sx={{
            display: "flex",
            flexDirection: { lg: "row", md: "row", sm: "column", xs: "column" },
            gap: 1,
            width: "100%",
          }}
        >
          {trainData.length ? (
            <svg
              ref={ref}
              style={{
                backgroundColor: colors.lightPred[1000],
                padding: 5,
                width: "100%",
                height: "400px",
                borderRadius: "10px",
              }}
              viewBox={`0 0 ${bounds.width} ${bounds.height}`}
            >
              {yScale.ticks().map((max) => {
                return (
                  <g key={max}>
                    <line
                      x1={margin.left}
                      x2={width - margin.right}
                      y1={yScale(max)}
                      y2={yScale(max)}
                      stroke="rgba(255,255,255,0.2)"
                      strokeDasharray="1"
                    />
                    <text
                      fill="rgba(255,255,255,0.3)"
                      alignmentBaseline="middle"
                      y={yScale(max)}
                    >
                      {max}
                    </text>
                  </g>
                );
              })}

              {months.map((date, i) => (
                <g key={i} transform={`translate(${xScale(date)},0)`}>
                  <text
                    className="yticks"
                    x={(xScale(endOfYear(date)) - xScale(date)) / 2 - 60}
                    y={height - 5}
                    textAnchor="middle"
                    fill="rgba(255,255,255,0.3)"
                  >
                    {format(date, "MMM y")}
                  </text>
                </g>
              ))}

              <motion.path
                initial={{ pathLength: 0 }}
                animate={{ pathLength: 1 }}
                transition={{ duration: 5, type: "spring" }}
                d={d}
                fill="none"
                stroke={colors.lightPred[700]}
                className="shadow"
              />

              <motion.path
                initial={{ pathLength: 0 }}
                animate={{ pathLength: 1 }}
                transition={{ duration: 5, type: "spring" }}
                d={v}
                fill="none"
                stroke={colors.lightPred[800]}
              />

              <motion.path
                initial={{ pathLength: 0 }}
                animate={{ pathLength: 1 }}
                transition={{ duration: 5, type: "spring" }}
                d={p}
                fill="none"
                stroke={colors.lightPred[900]}
              />
            </svg>
          ) : null}

          <TableContainer
            sx={{ width: { lg: "30%" }, height: "405px", borderRadius: "10px" }}
          >
            <Table sx={{ maxWidth: 600 }}>
              <TableHead sx={{ bgcolor: colors.lightPred[1100] }}>
                <TableRow sx={{ width: 0 }}>
                  <TableCell sx={{ width: 0, color: colors.lightPred[500] }}>
                    Date
                  </TableCell>
                  <TableCell
                    sx={{ width: 0, color: colors.lightPred[500] }}
                    align="left"
                  >
                    Close Price
                  </TableCell>
                  <TableCell
                    sx={{ width: "20px", color: colors.lightPred[500] }}
                    align="left"
                  >
                    Prediction
                  </TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
              {tableData.map((row) => (
                  <TableRow
                    key={row.date.toString()}
                    sx={{
                      "&:last-child td, &:last-child th": { border: 0 },
                    }}
                  >
                    <TableCell
                      sx={{ width: 0, color: colors.lightPred[500] }}
                      component="th"
                      scope="row"
                    >
                      {`${row.date.getFullYear()}-${row.date.getMonth()}-${row.date.getDay()}`}
                    </TableCell>
                    <TableCell
                      sx={{ width: 0, color: colors.lightPred[500] }}
                      align="left"
                    >
                      {row.price}
                    </TableCell>
                    <TableCell
                      sx={{ width: 0, color: colors.lightPred[500] }}
                      align="left"
                    >
                      {row.predict}
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        </Box>

        {/* Table Data */}
      </Box>
      <Prediction />
    </Box>
  );
}
