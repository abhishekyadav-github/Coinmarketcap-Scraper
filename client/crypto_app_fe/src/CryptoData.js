import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './cryptoDataStyles.css';

const ITEMS_PER_PAGE = 50;

const CryptoData = () => {
  const [data, setData] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(0);


const fetchData = async () => {
    try {
    const response = await axios.get('http://localhost:8000/api/latest_data/');
    const orderedDictList = response.data; // Assuming the data is a list of ordered dictionaries
    const transformedData = transformData(orderedDictList);
    setData(transformedData);
    setTotalPages(Math.ceil(transformedData.length / ITEMS_PER_PAGE));
    } catch (error) {
    console.error('Error fetching data:', error);
    }
};

const handlePageChange = (page) => {
    setCurrentPage(page);
    };

useEffect(() => {
    // Fetch data initially when the component mounts
    fetchData();

    // Set up an interval to fetch data every 3 seconds
    const interval = setInterval(fetchData, 3000);

    // Clean up the interval when the component unmounts
    return () => clearInterval(interval);
    }, []);


const startIndex = (currentPage - 1) * ITEMS_PER_PAGE;
const paginatedData = data.slice(startIndex, startIndex + ITEMS_PER_PAGE);

return (
<div>
    <h1 className="mb-4">Crypto Data</h1>
    <div className="table-responsive">
        <table className="crypto-table">
        <thead>
            <tr>
            <th> # </th>
            <th>Name</th>
            <th>Price</th>
            <th>1h%</th>
            <th>24h%</th>
            <th>7d%</th>
            <th>Market Cap</th>
            <th>Volume(24h)</th>
            <th>Circulating Supply</th>
            </tr>
        </thead>
        <tbody>
            {paginatedData.map((crypto, index) => (
            <tr key={crypto.id}>
                <td>{startIndex + index + 1}</td>
                <td>{crypto.name}</td>
                <td>{crypto.price}</td>
                <td>{crypto.percent_change_1h}</td>
                <td>{crypto.percent_change_24h}</td>
                <td>{crypto.percent_change_7d}</td>
                <td>{crypto.market_cap}</td>
                <td>{crypto.volume_24h}</td>
                <td>{crypto.circulating_supply}</td>
            </tr>
            ))}
        </tbody>
        </table>
    </div>
    <div>
    {Array.from({ length: totalPages }, (_, index) => (
        <button
        key={index + 1}
        onClick={() => handlePageChange(index + 1)}
        disabled={index + 1 === currentPage}
        >
        {index + 1}
        </button>
    ))}
    </div>
</div>
);
};


function transformData(orderedDictList) {
    return orderedDictList.map(item => ({
      id: item.id,
      name: item.name,
      price: item.price,
      percent_change_1h: item.percent_change_1h,
      percent_change_24h: item.percent_change_24h,
      percent_change_7d: item.percent_change_7d,
      market_cap: item.market_cap,
      volume_24h: item.volume_24h,
      circulating_supply: item.circulating_supply,
      data: item, // Considering the data from the backend is already in ordered dictionary format
    }));
}


export default CryptoData;