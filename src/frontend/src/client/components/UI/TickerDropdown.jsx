import React, { useState, useEffect } from 'react';
// import ticker from "@assets/data/tickerData";  // Đảm bảo đường dẫn chính xác
import "@client/styles/dropdown.css"
import useAxios from '@utils/useAxios'

const TickerDropdown = (props) => {
  const [isOpen, setIsOpen] = useState(false);
  const [selectedTicker, setSelectedTicker] = useState('Select a ticker');
  const [ticker, setTicker]=useState([]);
  const company = useAxios();


  useEffect(() => {
    const ListVN30 = async () => {
      try {
        const res = await company.get("/stock/stocktracking/list_companyVN30/");
        console.log(res.data.companies);
        setTicker(res.data.companies)
      } catch (error) {
          console.error('Có lỗi xảy ra khi truy cập dữ liệu:', error);
          
      }
    };
    ListVN30()

   }, []);
  const updateSymbol= async(symbol) => {
    try {
        const response = await company.post('/stock/stocktracking/update_symbol/', {
            symbol: symbol,
        });
        console.log('đã cập nhật thành công')
    } catch (error) {
        console.error('There was an error fetching the data!', error);
    }
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
              key={`${tickerItem}-${index}`} // Tạo key duy nhất
              className="dropdown-item"
              onClick={() => handleSelect(tickerItem)} // Sử dụng tickerItem trực tiếp
            >
              {tickerItem} {/* Hiển thị tickerItem trực tiếp */}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default TickerDropdown;
