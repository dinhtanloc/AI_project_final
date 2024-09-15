import React, { useState } from 'react';
import ticker from "@assets/data/tickerData";  // Đảm bảo đường dẫn chính xác
import "@styles/dropdown.css"

const TickerDropdown = (props) => {
  const [isOpen, setIsOpen] = useState(false);
  const [selectedTicker, setSelectedTicker] = useState('Select a ticker');

  const toggleDropdown = () => {
    setIsOpen(!isOpen);
  };

  const handleSelect = (ticker) => {
    setSelectedTicker(ticker);
    setIsOpen(false);
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
          {ticker.map((tickerItem) => (
            <div
              key={tickerItem.ticker}
              className="dropdown-item"
              onClick={() => handleSelect(tickerItem.ticker)}
            >
              {tickerItem.ticker}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default TickerDropdown;
