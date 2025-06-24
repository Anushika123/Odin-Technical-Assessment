import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

function Upload() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleUpload = async () => {
    if (!file) return alert('Please select a file');

    const formData = new FormData();
    formData.append('file', file);

    setLoading(true);
    try {
      const res = await axios.post(
        'http://localhost:5000/api/forecast',
        formData
      );
      localStorage.setItem('forecastResults', JSON.stringify(res.data));
      navigate('/result');
    } catch (err) {
      alert('Upload failed.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container py-5">
      <div className="row justify-content-center">
        <div className="col-md-8 col-lg-6">
          <div className="card shadow-sm border-0 rounded-4">
            <div className="card-body p-4">
              <h2 className="mb-4 text-center text-primary fw-semibold">
                Hospital Supply Forecast
              </h2>
              <p className="text-muted text-center mb-4">
                Upload your weekly usage data (.xlsx) to forecast the next 8
                weeks
              </p>

              <div className="mb-3">
                <label htmlFor="fileInput" className="form-label fw-medium">
                  Upload File
                </label>
                <input
                  type="file"
                  id="fileInput"
                  className="form-control"
                  onChange={e => setFile(e.target.files[0])}
                />
              </div>

              <button
                className="btn btn-primary w-100 fw-bold"
                onClick={handleUpload}
                disabled={loading}
              >
                {loading ? 'Uploading...' : 'Upload & Forecast'}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Upload;
