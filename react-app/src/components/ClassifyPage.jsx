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
            <div className="sample-card" key={sample.id}>
              <img src={sample.imagePath} alt={sample.name} />
              <h3>{sample.name}</h3>
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
