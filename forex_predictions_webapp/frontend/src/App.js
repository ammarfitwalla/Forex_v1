import React from 'react';
import './App.css';
import PredictionTable from './components/PredictionTable';
import PredictionChart from './components/PredictionChart';

function App() {
  return (
    <div className="App">
      <h1>Forex Prediction Dashboard</h1>
      <PredictionTable />
      <PredictionChart symbol="EURUSD" />
    </div>
  );
}

export default App;
