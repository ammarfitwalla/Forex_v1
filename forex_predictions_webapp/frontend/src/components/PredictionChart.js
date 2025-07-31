import React, { useEffect, useState } from 'react';
import { Line } from 'react-chartjs-2';
import axios from 'axios';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';

// Register Chart.js components
ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

const PredictionChart = ({ symbol }) => {
  const [chartDataHigh, setChartDataHigh] = useState(null);
  const [chartDataLow, setChartDataLow] = useState(null);

  const fetchPredictionData = () => {
    axios
      .get(`http://127.0.0.1:8000/api/predictions/${symbol}/`)
      .then((response) => {
        const data = response.data;
        if (data && data.length > 0) {
          const labels = data.map((item) => new Date(item.forecast_time).toLocaleString());

          // Round high and low forecasts to 6 decimal places
          const predictedHigh = data.map((item) => parseFloat(item.high_forecast.toFixed(6)));
          const predictedLow = data.map((item) => parseFloat(item.low_forecast.toFixed(6)));

          // Round actual high and low to 6 decimal places, keeping null for missing values
          const actualHigh = data.map((item) => (item.actual_high ? parseFloat(item.actual_high.toFixed(6)) : null));
          const actualLow = data.map((item) => (item.actual_low ? parseFloat(item.actual_low.toFixed(6)) : null));

          // Set chart data for high forecasts and actuals
          setChartDataHigh({
            labels,
            datasets: [
              {
                label: 'Predicted High',
                data: predictedHigh,
                borderColor: 'rgba(255, 99, 132, 0.8)',
                borderWidth: 2,
                borderDash: [5, 5],
                fill: false,
              },
              {
                label: 'Actual High',
                data: actualHigh,
                borderColor: 'rgba(75, 192, 192, 0.8)',
                borderWidth: 2,
                fill: false,
              },
            ],
          });

          // Set chart data for low forecasts and actuals
          setChartDataLow({
            labels,
            datasets: [
              {
                label: 'Predicted Low',
                data: predictedLow,
                borderColor: 'rgba(54, 162, 235, 0.8)',
                borderWidth: 2,
                borderDash: [5, 5],
                fill: false,
              },
              {
                label: 'Actual Low',
                data: actualLow,
                borderColor: 'rgba(153, 102, 255, 0.8)',
                borderWidth: 2,
                fill: false,
              },
            ],
          });
        } else {
          setChartDataHigh(null);
          setChartDataLow(null);
        }
      })
      .catch((error) => {
        console.error('Error fetching prediction data:', error);
        setChartDataHigh(null);
        setChartDataLow(null);
      });
  };

  useEffect(() => {
    fetchPredictionData();

    const interval = setInterval(() => {
      fetchPredictionData();
    }, 120000); // 2 minutes interval to refresh data

    return () => clearInterval(interval);
  }, [symbol]);

  return (
    <div style={{ width: '90%', padding: '20px' , justifySelf: 'center'}}>
      <div style={{ marginBottom: '40px', width: '100%' }}>
        {/* Chart for High predictions */}
        {chartDataHigh ? (
          <Line
            data={chartDataHigh}
            options={{
              responsive: true,
              plugins: {
                title: {
                  display: true,
                  text: `High Predictions vs Actuals for ${symbol}`,
                },
                tooltip: {
                  mode: 'index',
                  intersect: false,
                },
                legend: {
                  position: 'top',
                },
              },
              scales: {
                x: {
                  title: {
                    display: true,
                    text: 'Forecast Time',
                  },
                  reverse: true, // Reverse the x-axis to show the latest predictions first
                },
                y: {
                  beginAtZero: false,
                  title: {
                    display: true,
                    text: 'Price',
                  },
                  suggestedMin: 1.15,  // Adjust this based on your data
                  suggestedMax: 1.16,  // Adjust this based on your data
                  stepSize: 0.1,       // Set step size to 0.1 for finer price increments
                },
              },
            }}
            height={40}  // Set a smaller height for better compatibility with the screen
            width="100%"  // Set width to 100% for responsiveness
          />
        ) : (
          <p>No data available or error loading chart.</p>
        )}
      </div>

      <div>
        {/* Chart for Low predictions */}
        {chartDataLow ? (
          <Line
            data={chartDataLow}
            options={{
              responsive: true,
              plugins: {
                title: {
                  display: true,
                  text: `Low Predictions vs Actuals for ${symbol}`,
                },
                tooltip: {
                  mode: 'index',
                  intersect: false,
                },
                legend: {
                  position: 'top',
                },
              },
              scales: {
                x: {
                  title: {
                    display: true,
                    text: 'Forecast Time',
                  },
                  reverse: true, // Reverse the x-axis to show the latest predictions first
                },
                y: {
                  beginAtZero: false,
                  title: {
                    display: true,
                    text: 'Price',
                  },
                  suggestedMin: 1.15,  // Adjust this based on your data
                  suggestedMax: 1.16,  // Adjust this based on your data
                  stepSize: 0.01,       // Set step size to 0.01 for finer price increments
                },
              },
            }}
            height={40}  // Set a smaller height for better compatibility with the screen
            width="100%"  // Set width to 100% for responsiveness
          />
        ) : (
          <p>No data available or error loading chart.</p>
        )}
      </div>
    </div>
  );
};

export default PredictionChart;
