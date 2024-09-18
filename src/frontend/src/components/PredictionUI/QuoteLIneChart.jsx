import React, { useEffect, useState } from "react";
import * as d3 from "d3";
import useMeasure from "react-use-measure";
import useData from "@context/dataContext";
import { Box, Tooltip } from "@mui/material";
import { motion } from "framer-motion";
import {
  format,
  startOfMonth,
  endOfMonth,
  endOfYear,
  eachYearOfInterval,
  getYear,
} from "date-fns";
import { useTheme } from "@mui/material";
import { tokens } from "@theme";
export default function QuoteLIneChart() {
  const [circules, setCircules] = useState([]);
  
  function getCircules() {
    if (parseData.length > 0) {
      const groupsYear = {};
      parseData.forEach((val) => {
        const date = getYear(val.date);
        if (groupsYear[date]) {
          groupsYear[date].push(val);
        } else {
          groupsYear[date] = [val];
        }
      });

      const dataCircules = Object.values(groupsYear).map((val) => {
        return val.reduce((prev, current) => (prev.value > current.value ? prev : current));
      });

      setCircules(dataCircules);
    }
  }

  const { priceHistory, timeSeries, getParseData } = useData();

  const parseData = priceHistory.map((value, ind) => ({
    date: new Date(timeSeries[ind]),
    value,
  }));

  useEffect(() => {
    getParseData(parseData);
  }, [getParseData, parseData]);

  useEffect(() => {
    getCircules();
  }, [priceHistory]);

  const [ref, bounds] = useMeasure();
  const height = bounds.height;
  const width = bounds.width;
  const margin = {
    top: 20,
    right: 20,
    bottom: 25,
    left: 30,
  };

  const startDay = startOfMonth(parseData[0]?.date || new Date());
  const endDay = endOfMonth(parseData[parseData.length - 1]?.date || new Date());
  const months = eachYearOfInterval({ start: startDay, end: endDay });

  const xScale = d3
    .scaleTime()
    .domain([startDay, endDay])
    .range([margin.left, width - margin.right]);

  const yScale = d3
    .scaleLinear()
    .domain(d3.extent(parseData.map((d) => d.value)))
    .range([height - margin.bottom, margin.top]);

  const line = d3
    .line()
    .x((d) => xScale(d.date))
    .y((d) => yScale(d.value));

  const pathData = line(parseData);

  useEffect(() => {
    drawPulsatingCircle();
  }, []);

  const drawPulsatingCircle = () => {
    (function repeat() {
      d3.selectAll(".circle")
        .transition()
        .duration(300)
        .attr("stroke-width", 0)
        .attr("stroke-opacity", 0)
        .transition()
        .duration(300)
        .attr("stroke-width", 0)
        .attr("stroke-opacity", 0.5)
        .transition()
        .duration(1000)
        .attr("stroke-width", 25)
        .attr("stroke-opacity", 0)
        .ease(d3.easeSin)
        .on("end", repeat);
    })();
  };
  const theme = useTheme();
  const colors = tokens(theme.palette.mode);

  return (
    <Box
      sx={{
        width: { lg: "85%", md: "85%", sm: "95%", xs: "95%" },
        height: "400px",
        display: "flex",
        justifyContent: "flex-start",
        alignItems: "center",
        flexDirection: "column",
        pt: 5,
      }}
    >
      {parseData.length ? (
        <svg
          ref={ref}
          style={{
            backgroundColor: colors.lightPred[1000],
            padding: 5,
            width: "100%",
            height: "100%",
            borderRadius: "10px",
          }}
          viewBox={`0 0 ${bounds.width} ${bounds.height}`}
        >

          {yScale.ticks().map((max) => (
            <g key={max}>
              <line
                x1={margin.left}
                x2={width - margin.right}
                y1={yScale(max)}
                y2={yScale(max)}
                stroke={colors.lightPred[1600]}
                strokeDasharray="1"
              />
              <text
                fill={colors.lightPred[1700]}
                alignmentBaseline="middle"
                y={yScale(max)}
              >
                {max}
              </text>
            </g>
          ))}

          {months.map((date, i) => (
            <g key={i} transform={`translate(${xScale(date)},0)`}>
              {i % 2 === 1 && (
                <rect
                  width={xScale(endOfYear(date)) - xScale(date)}
                  height={height - margin.bottom}
                  fill={colors.lightPred[1400]}
                />
              )}
              <text
                className="yticks"
                x={(xScale(endOfYear(date)) - xScale(date)) / 2}
                y={height - 5}
                textAnchor="middle"
                fill={colors.lightPred[1200]}
              >
                {format(date, "MMM y")}
              </text>
            </g>
          ))}


          <motion.path
            className="shadow"
            initial={{ pathLength: 0 }}
            animate={{ pathLength: 1 }}
            transition={{ duration: 8, type: "spring" }}
            d={pathData}
            fill="none"
            stroke={colors.lightPred[700]}
          />

          {circules.map((d) => (
            <Tooltip
              key={d.value}
              title={`Close price: ${d.value.toFixed(2)}`}
              componentsProps={{
                tooltip: {
                  sx: {
                    bgcolor: colors.lightPred[1300],
                    fontSize: 15,
                  },
                },
              }}
            >
              <circle
                className="circle"
                key={d.date.toString()}
                stroke={colors.lightPred[1500]}
                fill={colors.lightPred[1500]}
                r="8"
                cx={xScale(d.date)}
                cy={yScale(d.value)}
              />
            </Tooltip>
          ))}
        </svg>
      ) : (
        <h2>Select a stock</h2>
      )}
    </Box>
  );
}
