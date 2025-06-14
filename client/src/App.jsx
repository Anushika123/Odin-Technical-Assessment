import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Upload from './components/upload';
import Result from './components/result';

function App() {
  return (
    <Routes>
      <Route path="/" element={<Upload />} />
      <Route path="/result" element={<Result />} />
    </Routes>
  );
}

export default App;
