import React from 'react';
import './App.css';
import PredictionTable from './components/PredictionTable';
import PredictionChart from './components/PredictionChart';
import AccuracySummary from './components/AccuracySummary';

function App() {
  return (
    <div className="App">
      <h1>Forex Prediction Dashboard</h1>
      <PredictionTable />
      <AccuracySummary />
      <h2>Prediction Chart for EURUSD</h2>
      <PredictionChart symbol="EURUSD" />
    </div>
  );
}

export default App;
