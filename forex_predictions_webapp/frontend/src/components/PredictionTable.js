import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Pagination } from '@mui/material';

const PredictionTable = () => {
  const [predictions, setPredictions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);

  const fetchPredictions = async (pageNumber) => {
    setLoading(true);
    try {
      const response = await axios.get(`http://127.0.0.1:8000/api/latest/?page=${pageNumber}`);
      if (response.data && response.data.results) {
        setPredictions(response.data.results);
        setTotalPages(Math.ceil(response.data.count / 10));
      } else {
        setPredictions([]);
      }
    } catch (error) {
      console.error('Error fetching predictions:', error);
      setPredictions([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchPredictions(page);
    const interval = setInterval(() => {
      fetchPredictions(page);
    }, 120000);
    return () => clearInterval(interval);
  }, [page]);

  const uniquePredictions = predictions.filter(
    (p, index, self) => index === self.findIndex((x) => x.forecast_time === p.forecast_time)
  );

  if (loading) return <p>Loading...</p>;

  return (
    <div>
      <h2>Latest Forex Predictions</h2>

      <table border="1" style={{ width: '100%', textAlign: 'center', borderCollapse: 'collapse' }}>
        <thead style={{ background: '#f2f2f2' }}>
          <tr>
            <th>Symbol</th>
            <th>Forecast Time</th>
            <th>Predicted High</th>
            <th>Predicted Low</th>
            <th>Actual High</th>
            <th>Actual Low</th>
            <th>Met/Missed High</th>
            <th>Met/Missed Low</th>
            <th>High Accuracy (pips) %</th>
            <th>Low Accuracy (pips) %</th>
          </tr>
        </thead>
        <tbody>
          {Array.isArray(uniquePredictions) && uniquePredictions.length > 0 ? (
            uniquePredictions.map((prediction) => (
              <tr key={prediction.id} style={{ backgroundColor: prediction.actual_high === null ? '#fff3cd' : 'white' }}>
                <td>{prediction.symbol}</td>
                <td>{new Date(prediction.forecast_time).toLocaleString()}</td>
                <td>{prediction.high_forecast?.toFixed(6)}</td>
                <td>{prediction.low_forecast?.toFixed(6)}</td>
                <td>{prediction.actual_high ?? 'N/A'}</td>
                <td>{prediction.actual_low ?? 'N/A'}</td>
                <td style={{ color: prediction.met_or_missed_high === 'met' ? 'green' : prediction.met_or_missed_high === 'missed' ? 'red' : 'black' }}>
                  {prediction.met_or_missed_high ?? 'N/A'}
                </td>
                <td style={{ color: prediction.met_or_missed_low === 'met' ? 'green' : prediction.met_or_missed_low === 'missed' ? 'red' : 'black' }}>
                  {prediction.met_or_missed_low ?? 'N/A'}
                </td>
                <td>{prediction.high_accuracy_score?.toFixed(2) ?? 'N/A'}</td>
                <td>{prediction.low_accuracy_score?.toFixed(2) ?? 'N/A'}</td>
              </tr>
            ))
          ) : (
            <tr>
              <td colSpan="10">No predictions available.</td>
            </tr>
          )}
        </tbody>
      </table>

      <div style={{ marginTop: '20px', display: 'flex', justifyContent: 'center' }}>
        <Pagination count={totalPages} page={page} onChange={(event, value) => setPage(value)} color="primary" />
      </div>
    </div>
  );
};

export default PredictionTable;
