import React, { useState, useEffect, useContext } from 'react';
import "@client/styles/dropdown.css"
import useAxios from '@utils/useAxios'
import StockContext from "@context/StockContext";

const TickerDropdown = (props) => {
  const [isOpen, setIsOpen] = useState(false);
  const [selectedTicker, setSelectedTicker] = useState('Select a ticker');
  const [ticker, setTicker]=useState([]);
  const company = useAxios();
  const [socket, setSocket] = useState(null);
  const { setStockSymbol } = useContext(StockContext);




  useEffect(() => {
    const ListVN30 = async () => {
      try {
        const res = await company.get("/stock/stocktracking/list_companyVN30/");
        console.log(res)
        setTicker(res.data.companies)
      } catch (error) {
          console.error('Có lỗi xảy ra khi truy cập dữ liệu:', error);
          
      }
    };
    ListVN30()

   }, []);
  const updateSymbol= async(symbol) => {
    setStockSymbol(symbol)
    
}

  const toggleDropdown = () => {
    setIsOpen(!isOpen);
  };

  const handleSelect = async(ticker) => {
    setSelectedTicker(ticker);
    setIsOpen(false);
    await updateSymbol(ticker);
  };

  return (
    <div className="dropdown" >
      <button
        className={`dropdown-toggle ${isOpen ? 'active' : ''}`}
        onClick={toggleDropdown}
      >
        {selectedTicker}
      </button>
      {isOpen && (
        <div className="dropdown-menu">
          {ticker.map((tickerItem, index) => (
            <div
              key={`${tickerItem}-${index}`} 
              className="dropdown-item"
              onClick={() => handleSelect(tickerItem)} 
            >
              {tickerItem} 
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default TickerDropdown;
