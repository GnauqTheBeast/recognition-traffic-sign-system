import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';

function ClassifyPage() {
  const navigate = useNavigate();
  const [classifiedSamples, setClassifiedSamples] = useState([]);

  const handleNavigate = () => {
    navigate('/vision/classify');
  };

  useEffect(() => {
    const user = JSON.parse(localStorage.getItem('user'));
    const userId = user?.id;
    if (userId) {
      const saved = localStorage.getItem(`classifiedResults_${userId}`);
      const parsed = saved ? JSON.parse(saved) : [];
      setClassifiedSamples(parsed);
    }
  }, []);

  return (
    <div className="samples-container">
      <h2>Classified Samples</h2>
      <button className="action-button" onClick={handleNavigate}>
        Classify
      </button>
      <div className="samples-list">
        {classifiedSamples.length === 0 ? (
          <p>Chưa có mẫu nào được phân loại.</p>
        ) : (
          classifiedSamples.map(sample => (
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
              <p><strong>Label:</strong> {sample.signName}</p>
            </div>
          ))
        )}
      </div>
    </div>
  );
}

export default ClassifyPage;
