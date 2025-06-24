import React, { useEffect, useState } from 'react';
import {
  LineChart,
  Line,
  CartesianGrid,
  XAxis,
  YAxis,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';

function Result() {
  const [results, setResults] = useState({});

  useEffect(() => {
    const stored = localStorage.getItem('forecastResults');
    if (stored) {
      setResults(JSON.parse(stored));
    }
  }, []);

  return (
    <div className="container mt-4">
      <h2>Forecast Results</h2>
      {Object.entries(results).map(([itemCode, data]) => {
        const chartData = data.actual.map((actualVal, index) => ({
          week: `Week ${149 + index}`,
          Actual: actualVal,
          Predicted: data.predicted[index],
        }));

        return (
          <div className="card mb-4" key={itemCode}>
            <div className="card-body">
              <h5 className="card-title">Item Code: {itemCode}</h5>
              <p className="card-text">
                MAE: {data.mae} | MAPE: {data.mape}% | RMSE: {data.rmse}
              </p>

              <table className="table table-bordered mb-4">
                <thead>
                  <tr>
                    <th>Week</th>
                    <th>Actual</th>
                    <th>Predicted</th>
                  </tr>
                </thead>
                <tbody>
                  {chartData.map((row, i) => (
                    <tr key={i}>
                      <td>{row.week}</td>
                      <td>{row.Actual}</td>
                      <td>{row.Predicted}</td>
                    </tr>
                  ))}
                </tbody>
              </table>

              <h6>Actual vs Predicted Chart</h6>
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={chartData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="week" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Line type="monotone" dataKey="Actual" stroke="#8884d8" />
                  <Line type="monotone" dataKey="Predicted" stroke="#82ca9d" />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </div>
        );
      })}
    </div>
  );
}

export default Result;
