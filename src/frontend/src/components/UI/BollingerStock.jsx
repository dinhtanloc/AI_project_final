// BollingerStock.js
import React, { useState, useEffect, useRef } from 'react';
import * as Plot from '@observablehq/plot';
import getData from '@assets/data/stockData'; // Giả sử bạn đã có dữ liệu APPL

const BollingerStock = ({n,k}) => {
  // const [n, setN] = useState(20); // Periods
  // const [k, setK] = useState(2);  // Deviations
  const plotRef = useRef(null);
  const [aaplData,setData] = useState(getData())
  // console.log(aaplData)

  useEffect(() => {
    if (plotRef.current) {
      // Clear previous plots
      plotRef.current.innerHTML = '';

      // Render the plot
      const plot = Plot.plot({
        width: 850,
        height:300,
        y: { grid: true, label: "Stock Price (APPL)" },
        x: { label: "Date" },
        marks: [
          Plot.bollingerY(aaplData, { n, k, x: "date", y: "close", stroke: "none" }),
          Plot.lineY(aaplData, { x: "date", y: "close", strokeWidth: 1 }),
          Plot.lineY(aaplData, Plot.windowY({ k: 28, reduce: "min" }, { x: "date", y: "close", stroke: "blue" })),
          Plot.lineY(aaplData, Plot.windowY({ k: 28, reduce: "max" }, { x: "date", y: "close", stroke: "red" })),
          Plot.lineY(aaplData, Plot.windowY({ k: 28, reduce: "median" }, { x: "date", y: "close" }))
        ]
      });

      plotRef.current.appendChild(plot);
    }
  }, [n, k]);

  return (
    <div>
      {/* <div>
        <label>Periods (N):</label>
        <input
          type="range"
          min="2"
          max="100"
          step="1"
          value={n}
          onChange={(e) => setN(Number(e.target.value))}
        />
        <span>{n}</span>
      </div>
      <div>
        <label>Deviations (K):</label>
        <input
          type="range"
          min="0"
          max="4"
          step="0.1"
          value={k}
          onChange={(e) => setK(Number(e.target.value))}
        />
        <span>{k}</span>
      </div> */}
      <div ref={plotRef}></div>
    </div>
  );
};

export default BollingerStock;
