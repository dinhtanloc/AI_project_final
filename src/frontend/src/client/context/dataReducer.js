// Import necessary modules
// import { ClockNumberClassKey } from '@mui/x-date-pickers'; // Assuming this import is necessary, though it's not used in the code.
import { useReducer } from 'react';

// Enum replacement with plain object to simulate JavaScript enums
const PriceActionKind = {
  GET_PRICES: 'GET_PRICES',
  GET_TIME: 'GET_TIME',
  GET_TRAIN_PRICES: 'GET_TRAIN_PRICES',
  GET_TIMETRAIN: 'GET_TIMETRAIN',
  LOADING: 'LOADING',
  GET_CLOSE_PRICE: 'GET_CLOSE_PRICE',
  GET_PREDICTION_CLOSE: 'GET_PREDICTION_CLOSE',
  GET_TIME_PREDICTION: 'GET_TIME_PREDICTION',
  GET_PARSEDATA: 'GET_PARSEDATA',
  GET_RMSE: 'GET_RMSE',
  GET_PRED_PRICE: 'GET_PRED_PRICE'
};

// Initial state setup
const initialState = {
  // Prices History
  priceHistory: [],
  timeSeries: [],
  getHistoryPrices: () => {},
  getTimeSeries: () => {},

  // Train Prices
  priceTrain: [],
  timeTrain: [],
  getTrainPrices: () => {},
  getTrainTime: () => {},

  // Prediction Data
  priceClose: [],
  predictionClose: [],
  timePrediction: [],
  getPriceClose: () => {},
  getPredictionClose: () => {},
  getTimePrediction: () => {},

  // Parse Data
  parseData: [],
  getParseData: () => {},

  // RMSE
  rmse: [],
  getRmse: () => {},

  // Loading
  loading: false,
  Loading: () => {},

  // Predicted Price
  price: [],
  getPredPrice: () => {}
};

// Reducer function
const dataReducer = (state, action) => {
  const { type, payload } = action;
  
  switch (type) {
    // Price History
    case PriceActionKind.GET_PRICES:
      return {
        ...state,
        priceHistory: payload,
      };

    case PriceActionKind.GET_TIME:
      return {
        ...state,
        timeSeries: payload,
      };

    // Train Data
    case PriceActionKind.GET_TRAIN_PRICES:
      return {
        ...state,
        priceTrain: payload,
      };

    case PriceActionKind.GET_TIMETRAIN:
      return {
        ...state,
        timeTrain: payload,
      };

    // Table Data
    case PriceActionKind.GET_CLOSE_PRICE:
      return {
        ...state,
        priceClose: payload,
      };

    case PriceActionKind.GET_PREDICTION_CLOSE:
      return {
        ...state,
        predictionClose: payload,
      };

    case PriceActionKind.GET_TIME_PREDICTION:
      return {
        ...state,
        timePrediction: payload,
      };

    // Parse Data
    case PriceActionKind.GET_PARSEDATA:
      return {
        ...state,
        parseData: payload,
      };

    // RMSE
    case PriceActionKind.GET_RMSE:
      return {
        ...state,
        rmse: payload,
      };

    // Loading state
    case PriceActionKind.LOADING:
      return {
        ...state,
        loading: !state.loading,
      };

    // Predicted Price
    case PriceActionKind.GET_PRED_PRICE:
      return {
        ...state,
        price: payload,
      };

    default:
      return state;
  }
};

export { PriceActionKind, initialState, dataReducer };
