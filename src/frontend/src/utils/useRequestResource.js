import { useCallback, useContext } from "react";
import axios from "axios";
import useData from "@context/dataContext";
// import useAxios from './useAxios'
// Create an axios client with a base URL
// const client = useAxios()
const client = axios.create({
  baseURL: "http://127.0.0.1:8000/prediction/train",
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
          getHistoryPrices(res.data.prices);
          getTimeSeries(res.data.time);

          // Train Data
          getTrainTime(res.data.train.timeTrain);
          getTrainPrices(res.data.train.value);

          // Table Data
          getPriceClose(res.data.valid.value);
          getPredictionClose(res.data.valid.Predictions);
          getTimePrediction(res.data.valid.timeValid);

          // RMSE
          getRmse([res.data.rmse]);

          // Predicted prices
          getPredPrice(res.data.price);

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
