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
            <div className="sample-card" key={sample.id}>
              <img src={sample.imagePath} alt={sample.name} />
              <h3>{sample.name}</h3>
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
