import React, { createContext, useReducer, useContext } from "react";
import { dataReducer, initialState, PriceActionKind } from "./dataReducer";

const Context = createContext(initialState);

export function Provider({ children }) {
  const [state, dispatch] = useReducer(dataReducer, initialState);
  
  // Price History
  const getHistoryPrices = (value) => {
    dispatch({
      type: PriceActionKind.GET_PRICES,
      payload: value,
    });
  };
  console.log('import contexxt')

  const getTimeSeries = (value) => {
    dispatch({
      type: PriceActionKind.GET_TIME,
      payload: value,
    });
  };

  // Train data
  const getTrainPrices = (value) => {
    dispatch({
      type: PriceActionKind.GET_TRAIN_PRICES,
      payload: value,
    });
  };

  const getTrainTime = (value) => {
    dispatch({
      type: PriceActionKind.GET_TIMETRAIN,
      payload: value,
    });
  };

  // Table Data
  const getPriceClose = (value) => {
    dispatch({
      type: PriceActionKind.GET_CLOSE_PRICE,
      payload: value,
    });
  };

  const getPredictionClose = (value) => {
    dispatch({
      type: PriceActionKind.GET_PREDICTION_CLOSE,
      payload: value,
    });
  };

  const getTimePrediction = (value) => {
    dispatch({
      type: PriceActionKind.GET_TIME_PREDICTION,
      payload: value,
    });
  };

  // Parse Data
  const getParseData = (value) => {
    dispatch({
      type: PriceActionKind.GET_PARSEDATA,
      payload: value,
    });
  };

  // Get RMSE
  const getRmse = (value) => {
    dispatch({
      type: PriceActionKind.GET_RMSE,
      payload: value,
    });
  };

  const Loading = () => {
    dispatch({
      type: PriceActionKind.LOADING,
      payload: [],
    });
  };

  const getPredPrice = (value) => {
    dispatch({
      type: PriceActionKind.GET_PRED_PRICE,
      payload: value,
    });
  };

  const contextValue = {
    // Price History
    priceHistory: state.priceHistory,
    timeSeries: state.timeSeries,
    getHistoryPrices,
    getTimeSeries,

    // Train Data
    priceTrain: state.priceTrain,
    timeTrain: state.timeTrain,
    getTrainPrices,
    getTrainTime,

    // Prediction Data
    priceClose: state.priceClose,
    predictionClose: state.predictionClose,
    timePrediction: state.timePrediction,
    getPriceClose,
    getPredictionClose,
    getTimePrediction,

    // Parse Data
    parseData: state.parseData,
    getParseData,

    // RMSE
    rmse: state.rmse,
    getRmse,

    // Loading
    loading: state.loading,
    Loading,

    // Pred Price
    price: state.price,
    getPredPrice,
  };

  return <Context.Provider value={contextValue}>{children}</Context.Provider>;
}

// Context
const useData = () => {
  const context = useContext(Context);
  return context;
};

export default useData;
