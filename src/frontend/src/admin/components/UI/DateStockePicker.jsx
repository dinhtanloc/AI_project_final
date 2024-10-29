import React, { useState, useEffect } from "react";
import useRequestResource from "@utils/useRequestResource";
import { DesktopDatePicker } from "@mui/x-date-pickers/DesktopDatePicker";
import { LocalizationProvider } from "@mui/x-date-pickers/LocalizationProvider";
import { AdapterDayjs } from "@mui/x-date-pickers/AdapterDayjs";
import { format } from "date-fns";
import {
  Box,
  Typography,
  TextField,
  Stack,
  InputLabel,
  MenuItem,
  FormControl,
  Select,
  Snackbar,
  Button,
} from "@mui/material";
import { useTheme } from "@mui/material";
import { tokens } from "@theme";
import useAxios from '@utils/useAxios'
export default function DateStockPicker() {
  const theme = useTheme();
  const colors = tokens(theme.palette.mode);
  const [open, setOpen] = useState(false);
  const { getResourceData } = useRequestResource();
  const [startDate, setStartDate] = useState("");
  const [stockMenu,setstockMenu]=useState([]);
  const ticket=useAxios();
  useEffect(() => {
    const ListVN30 = async () => {
      try {
        const res = await ticket.get("/stock/stocktracking/list_companyVN30/");
        setstockMenu(res.data.companies)
      } catch (error) {
          console.error('Có lỗi xảy ra khi truy cập dữ liệu:', error);
          
      }
    };
    ListVN30()

   }, []);
  const handleChangeStart = (start) => {
    setStartDate(format(new Date(start), "yyyy-MM-dd"));
  };
  const [endDate, setEndDate] = useState("");
  const handleChangeEnd = (end) => {
    setEndDate(format(new Date(end), "yyyy-MM-dd"));
  }; 
  const [stock, setStock] = useState("");
  const handleChangeStock = (event) => {
    setStock(event.target.value);
  };
  const [interval, setInterval] = useState("");
  const handleChangeInterval = (event) => {
    setInterval(event.target.value);
  };

  const handleClose = () => {
    setOpen(false);
  };

  const [request, setRequest] = useState(false);

  const action = (
    <React.Fragment>
      <Button sx={{ color: colors.lightPred[600] }} size="small" onClick={handleClose}>
        Close
      </Button>
    </React.Fragment>
  );


  let totalDays =
    (new Date(endDate).getTime() - new Date(startDate).getTime()) /
    (1000 * 3600 * 24);

  useEffect(() => {
    if (stock !== "") {
      getResourceData({
        query: `?start=${startDate}&end=${endDate}&symbol=${stock}&interval=${interval}`,
      });
    } else {
      stock !== "" ? setOpen(true) : null;
    }
  }, [stock, request]);


  const intervalMenu = ["1m", "1D", "1W", "1M"];

  return (
    <LocalizationProvider dateAdapter={AdapterDayjs}>
      <Snackbar
        open={open}
        autoHideDuration={6000}
        onClose={handleClose}
        message="Date range not allowed, enter a range more than 1 year"
        action={action}
      />
      <Typography
        variant="h3"
        sx={{
          pb: 5,
          fontFamily: "Roboto Flex",
          color: colors.lightPred[500],
          fontSize: { lg: 45, md: 45, sm: 35, xs: 25 },
        }}
      >
        Close Price History
      </Typography>
      <Stack
        spacing={{ lg: 3, md: 3, sm: 0, xs: 0 }}
        direction="row"
        sx={{ pb: 2 }}
      >
        <DesktopDatePicker
          label="Start Date"
          inputFormat="MM/DD/YYYY"
          value={startDate}
          onChange={handleChangeStart}
          renderInput={(params) => <TextField {...params} />}
        />
        <DesktopDatePicker
          label="End Date"
          inputFormat="MM/DD/YYYY"
          value={endDate}
          onChange={handleChangeEnd}
          renderInput={(params) => <TextField {...params} />}
        />
        <Box sx={{ minWidth: 120 }}>
          <FormControl fullWidth>
            <InputLabel
              id="stock-label"
              sx={{ color: colors.lightPred[400] }}
            >
              Interval
            </InputLabel>
           
            <Select
              sx={{ color: colors.lightPred[400] }}
              id="demo-simple-select"
              value={interval}
              label="Interval"
              onChange={handleChangeInterval}
            >
              {intervalMenu.map((interval) => (
                <MenuItem
                  key={interval}
                  value={interval}
             
                >
                  {interval}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
        </Box>
        <Box sx={{ minWidth: 120 }}>
          <FormControl fullWidth>
            <InputLabel
              id="stock-label"
              sx={{ color: colors.lightPred[400] }}
            >
              Stock
            </InputLabel>
            <Select
              sx={{ color: colors.lightPred[400] }}
              id="demo-simple-select"
              value={stock}
              label="Stock"
              onChange={handleChangeStock}
            >
              {stockMenu.map((stock) => (
                <MenuItem
                  key={stock}
                  value={stock}
                  // onClick={() => setRequest(!request)}
                >
                  {stock}
                </MenuItem>
              ))}
            </Select>
           
          </FormControl>
        </Box>
      </Stack>
    </LocalizationProvider>
  );
}
