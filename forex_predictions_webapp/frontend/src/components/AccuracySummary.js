import React, { useEffect, useState } from 'react';
import axios from 'axios';

const AccuracySummary = () => {
  const [summary, setSummary] = useState([]);
  const [loading, setLoading] = useState(true);

const fetchSummary = async () => {
  try {
    const response = await axios.get('http://127.0.0.1:8000/api/accuracy-summary/');
    console.log("API response:", response.data);
    setSummary(response.data.summary || []);  // or response.data if it's an array
  } catch (error) {
    console.error('Error fetching accuracy summary:', error);
    setSummary([]);
  } finally {
    setLoading(false);
  }
};
    

  useEffect(() => {
    fetchSummary();

    const interval = setInterval(() => {
      fetchSummary();
    }, 120000); // 2-minute interval

    return () => clearInterval(interval); // cleanup
  }, []);

  if (loading) return <p>Loading summary...</p>;

  return (
    <div style={{ marginTop: '40px' }}>
      <h2>Accuracy Summary by Symbol</h2>
      <table border="1" style={{ width: '100%', textAlign: 'center', borderCollapse: 'collapse' }}>
        <thead style={{ background: '#f2f2f2' }}>
          <tr>
            <th>Symbol</th>
            <th>Last 'n' Predictions</th>
            <th>High Met %</th>
            <th>Low Met %</th>
            <th>Avg High Accuracy</th>
            <th>Avg Low Accuracy</th>
          </tr>
        </thead>
        <tbody>
          {summary.map((item, index) => (
            <tr key={index}>
              <td>{item.symbol}</td>
              <td>{item.total_predictions}</td>
              <td style={{ color: item.high_met_percentage >= 50 ? 'green' : 'red' }}>
                {item.high_met_percentage}%
              </td>
              <td style={{ color: item.low_met_percentage >= 50 ? 'green' : 'red' }}>
                {item.low_met_percentage}%
              </td>
              <td>{item.avg_high_accuracy_score}</td>
              <td>{item.avg_low_accuracy_score}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default AccuracySummary;
