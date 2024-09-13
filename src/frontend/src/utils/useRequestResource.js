import { useCallback, useContext } from "react";
import axios from "axios";
import useData from "@context/dataContext";

// Create an axios client with a base URL
const client = axios.create({
  baseURL: "http://127.0.0.1:8000/prediction",
});

// Custom hook to request resources
export default function useRequestResource() {
  // Destructuring methods from useData context
  const {
    getHistoryPrices,
    getTimeSeries,
    getTrainTime,
    getTrainPrices,
    getPriceClose,
    getPredictionClose,
    getTimePrediction,
    getRmse,
    Loading,
    getPredPrice,
  } = useData();

  // Define the getResourceData function with useCallback to memoize it
  const getResourceData = useCallback(
    ({ query }) => {
      // Toggle loading state
      Loading();

      // Make a GET request to the API endpoint
      client
        .get(`${query}`)
        .then((res) => {
          // Update state with received data

          // History Prices
          getHistoryPrices(res.data.data.prices);
          getTimeSeries(res.data.data.time);

          // Train Data
          getTrainTime(res.data.data.train.timeTrain);
          getTrainPrices(res.data.data.train.Close);

          // Table Data
          getPriceClose(res.data.data.valid.Close);
          getPredictionClose(res.data.data.valid.Predictions);
          getTimePrediction(res.data.data.valid.timeValid);

          // RMSE
          getRmse([res.data.data.rmse]);

          // Predicted prices
          getPredPrice(res.data.data.price);

          // Toggle loading state
          Loading();
        })
        .catch((err) => console.log(err));
    },
    [Loading, getHistoryPrices, getTimeSeries, getTrainTime, getTrainPrices, getPriceClose, getPredictionClose, getTimePrediction, getRmse, getPredPrice]
  );

  // Return the getResourceData function
  return {
    getResourceData,
  };
}
