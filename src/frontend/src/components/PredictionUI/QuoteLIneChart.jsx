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

export default function QuoteLIneChart() {
  // Getting circles data (max value by year)
  const [circules, setCircules] = useState([]);
  
  function getCircules() {
    if (parseData.length > 0) {
      const groupsYear = {};
      
      // Grouping data by year
      parseData.forEach((val) => {
        const date = getYear(val.date);
        if (groupsYear[date]) {
          groupsYear[date].push(val);
        } else {
          groupsYear[date] = [val];
        }
      });

      // Extracting max values by year
      const dataCircules = Object.values(groupsYear).map((val) => {
        return val.reduce((prev, current) => (prev.value > current.value ? prev : current));
      });

      setCircules(dataCircules);
    }
  }

  // Destructuring data and methods from context
  const { priceHistory, timeSeries, getParseData } = useData();

  // Parsing price history into usable format
  const parseData = priceHistory.map((value, ind) => ({
    date: new Date(timeSeries[ind]),
    value,
  }));

  // Setting parsed data into context on load
  useEffect(() => {
    getParseData(parseData);
  }, [getParseData, parseData]);

  // Calculating circles data whenever price history changes
  useEffect(() => {
    getCircules();
  }, [priceHistory]);

  // Measuring the SVG dimensions for D3 rendering
  const [ref, bounds] = useMeasure();

  const height = bounds.height;
  const width = bounds.width;
  const margin = {
    top: 20,
    right: 20,
    bottom: 25,
    left: 30,
  };

  // Date intervals for the x-axis
  const startDay = startOfMonth(parseData[0]?.date || new Date());
  const endDay = endOfMonth(parseData[parseData.length - 1]?.date || new Date());
  const months = eachYearOfInterval({ start: startDay, end: endDay });

  // Scales for x and y axes
  const xScale = d3
    .scaleTime()
    .domain([startDay, endDay])
    .range([margin.left, width - margin.right]);

  const yScale = d3
    .scaleLinear()
    .domain(d3.extent(parseData.map((d) => d.value)))
    .range([height - margin.bottom, margin.top]);

  // Line generator for D3 path
  const line = d3
    .line()
    .x((d) => xScale(d.date))
    .y((d) => yScale(d.value));

  const pathData = line(parseData);

  // Pulsating circle animation
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
            backgroundColor: "#1A172C",
            padding: 5,
            width: "100%",
            height: "100%",
            borderRadius: "10px",
          }}
          viewBox={`0 0 ${bounds.width} ${bounds.height}`}
        >
          {/* Y Axis ticks and lines */}
          {yScale.ticks().map((max) => (
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
                fill="rgba(255,255,255,0.5)"
                alignmentBaseline="middle"
                y={yScale(max)}
              >
                {max}
              </text>
            </g>
          ))}

          {/* X Axis labels */}
          {months.map((date, i) => (
            <g key={i} transform={`translate(${xScale(date)},0)`}>
              {i % 2 === 1 && (
                <rect
                  width={xScale(endOfYear(date)) - xScale(date)}
                  height={height - margin.bottom}
                  fill="rgba(0,0,0,0.2)"
                />
              )}
              <text
                className="yticks"
                x={(xScale(endOfYear(date)) - xScale(date)) / 2}
                y={height - 5}
                textAnchor="middle"
                fill="rgba(255,255,255,0.5)"
              >
                {format(date, "MMM y")}
              </text>
            </g>
          ))}

          {/* Line chart */}
          <motion.path
            className="shadow"
            initial={{ pathLength: 0 }}
            animate={{ pathLength: 1 }}
            transition={{ duration: 8, type: "spring" }}
            d={pathData}
            fill="none"
            stroke="#03FFF9"
          />

          {/* Circles on line chart */}
          {circules.map((d) => (
            <Tooltip
              key={d.value}
              title={`Close price: ${d.value.toFixed(2)}`}
              componentsProps={{
                tooltip: {
                  sx: {
                    bgcolor: "black",
                    fontSize: 15,
                  },
                },
              }}
            >
              <circle
                className="circle"
                key={d.date.toString()}
                stroke="#E4FCFF"
                fill="#E4FCFF"
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
