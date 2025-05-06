import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import '../styles/SamplesPage.css';

function DetectPage() {
  const navigate = useNavigate();
  const [detectSamples, setDetectSamples] = useState([]);

  useEffect(() => {
    const user = JSON.parse(localStorage.getItem('user'));
    const userId = user?.id;
    const key = `detectedResults_${userId}`;
    const storedSamples = JSON.parse(localStorage.getItem(key)) || [];
    setDetectSamples(storedSamples);
  }, []);

  const handleNavigate = () => {
    navigate('/vision/detect');
  };

  return (
    <div className="samples-container">
      <h2>Detected Samples</h2>
      <button className="action-button" onClick={handleNavigate}>
        Detect
      </button>
      <div className="samples-list">
        {detectSamples.length === 0 ? (
          <p>No detected samples yet.</p>
        ) : (
          detectSamples.map(sample => (
            <div
              key={sample.id}
              style={{
                width: '200px',
                padding: '12px',
                border: '1px solid #ddd',
                borderRadius: '10px',
                textAlign: 'center',
                boxShadow: '0 2px 4px rgba(0, 0, 0, 0.1)',
                margin: '10px'
              }}
            >
              <img
                src={sample.imagePath}
                alt={sample.name}
                style={{
                  width: '100%',
                  height: 'auto',
                  borderRadius: '6px'
                }}
              />
              <h3 style={{ fontSize: '16px', margin: '8px 0 4px', color: '#333' }}>
                {sample.name}
              </h3>
              <p><strong>Date:</strong> {sample.date}</p>
              <p><strong>Model:</strong> {sample.modelUsed}</p>
              <p><strong>Box:</strong> {JSON.stringify(sample.boundingBox)}</p>
            </div>
          ))
        )}
      </div>
    </div>
  );
}

export default DetectPage;
