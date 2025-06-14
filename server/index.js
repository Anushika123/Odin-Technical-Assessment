const express = require('express');
const cors = require('cors');
const forecastRouter = require('./routes/forecast.js');

const app = express();
const PORT = 5000;

app.use(cors());
app.use('/api/forecast', forecastRouter);

app.listen(PORT, () =>
  console.log(`Server running on http://localhost:${PORT}`)
);
