import React, { useState } from 'react';

const SampleCard = ({ sample, type }) => {
  const [showDetails, setShowDetails] = useState(false);

  // Hiển thị bounding box nếu là mẫu detect
  const renderBoundingBox = () => {
    if (type === 'detect' && sample.boundingBox) {
      const { x1, y1, x2, y2 } = sample.boundingBox;
      const boxStyle = {
        position: 'absolute',
        left: `${x1 / 6}px`,
        top: `${y1 / 6}px`,
        width: `${(x2 - x1) / 6}px`,
        height: `${(y2 - y1) / 6}px`,
        border: '2px solid red',
        pointerEvents: 'none'
      };
      return <div style={boxStyle}></div>;
    }
    return null;
  };

  return (
    <div className="bg-white rounded-lg shadow-md overflow-hidden transition-transform hover:scale-105">
      <div className="relative">
        <img 
          src={sample.imagePath} 
          alt={sample.name} 
          className="w-full h-48 object-cover"
        />
        {renderBoundingBox()}
      </div>
      <div className="p-4">
        <h3 className="text-lg font-semibold mb-2">{sample.name}</h3>
        <p className="text-gray-600 mb-2">Ngày: {sample.date}</p>
        <p className="text-gray-600 mb-2">Model: {sample.modelUsed}</p>
        
        {type === 'classify' && (
          <div className="mb-2">
            <p className="text-gray-600">Nhãn: {sample.signName}</p>
            <p className="text-gray-600">Độ tin cậy: {(sample.confidence * 100).toFixed(2)}%</p>
          </div>
        )}
        
        <button
          onClick={() => setShowDetails(!showDetails)}
          className="text-blue-600 hover:text-blue-800 mt-2"
        >
          {showDetails ? 'Ẩn chi tiết' : 'Xem chi tiết'}
        </button>
        
        {showDetails && (
          <div className="mt-3 p-3 bg-gray-100 rounded">
            <h4 className="font-semibold mb-2">Thông tin biển báo:</h4>
            {sample.trafficSigns.map(sign => (
              <div key={sign.id} className="mb-1">
                <p>Loại: {sign.type}</p>
                <p>Nhãn: {sign.label}</p>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default SampleCard;
