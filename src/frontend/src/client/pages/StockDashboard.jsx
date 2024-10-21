import React, { useContext, useEffect, useState } from "react";
import ThemeContext from "@context/ThemeContext";
import Overview from "@client/components/UI/StockChart/Overview";
import Details from "@client/components/UI/StockChart/Details";
import Chart from "@client/components/UI/StockChart/Chart";
import Header from "@client/components/UI/StockChart/Header";
import StockContext from "@context/StockContext";
// import { fetchStockDetails, fetchQuote } from "@utils/api/stock-api";

const StockDashboard = () => {
  const { darkMode } = useContext(ThemeContext);

  const { stockSymbol } = useContext(StockContext);

  const [stockDetails, setStockDetails] = useState({});

  const [quote, setQuote] = useState({});

  useEffect(() => {
      // const fetchStockTracking = async () => {
      //   try {
      //     const res = await stock.get("/stock/stocktracking/historicaldata/");
          
      //     const formattedData = res.data.price_data.map(item => ({
      //       ...item,
      //       date: new Date(item.date), // Chuyển chuỗi thành Date object
      //       // open: parseFloat(item.open),
      //       // high: parseFloat(item.high),
      //       // low: parseFloat(item.low),
      //       // close: parseFloat(item.close),
      //       // volume: parseInt(item.volume, 10),
      //     }))
      //     // setName(res.data.company)
      //     // .filter(item => 
      //     //   item.high >= Math.max(item.open, item.close, item.low) &&
      //     //   item.low <= Math.min(item.open, item.close, item.high) 
      //     // );
          
      //     setQuote(formattedData);
      //     // setName(res.data.company);
      //   } catch (error) {
      //     console.error('Có lỗi xảy ra khi truy cập dữ liệu:', error);
      //   }
      // };
  
      // fetchStockTracking();

    const updateStockDetails = async () => {
    //   try {
    //     const result = await fetchStockDetails(stockSymbol);
    //     setStockDetails(result);
    //   } catch (error) {
    //     setStockDetails({});
    //     console.log(error);
    //   }
    };

    const updateStockOverview = async () => {
    //   try {
    //     const result = await fetchQuote(stockSymbol);
    //     setQuote(result);
    //   } catch (error) {
    //     setQuote({});
    //     console.log(error);
    //   }
    };

    updateStockDetails();
    updateStockOverview();
  }, [stockSymbol]);

  return (
    <div
      className={`h-screen grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 grid-rows-8 md:grid-rows-7 xl:grid-rows-5 auto-rows-fr gap-6 p-10 font-quicksand ${
        darkMode ? "bg-gray-900 text-gray-300" : "bg-neutral-100"
      }`}
    >
      {/* <div className="col-span-1 md:col-span-2 xl:col-span-3 row-span-1 flex justify-start items-center">
        <Header name={stockDetails.name} />
      </div> */}
      <div className="md:col-span-2 row-span-4">
        <Chart />
      </div>
      <div>
        <Overview
          symbol={stockSymbol}
          price={quote.pc}
          change={quote.d}
          changePercent={quote.dp}
          currency={stockDetails.currency}
        />
      </div>
      <div className="row-span-2 xl:row-span-3">
        <Details details={stockDetails} />
      </div>
    </div>
  );
};

export default StockDashboard;
