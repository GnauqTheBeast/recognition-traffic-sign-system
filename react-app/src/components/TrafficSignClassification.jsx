import React, { useState } from 'react';
import ImageUploader from '../components/ImageUploader';
import '../styles/TrafficSignClassification.css';

const TrafficSignClassification = () => {
    const [selectedImage, setSelectedImage] = useState(null);
    const [imageUrl, setImageUrl] = useState(null);
    const [classificationResult, setClassificationResult] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const handleImageUpload = (file) => {
        setSelectedImage(file);
        setImageUrl(URL.createObjectURL(file));
        setClassificationResult(null);
        setError(null);
    };

    const classifySign = async () => {
        if (!selectedImage) return;

        setLoading(true);
        setError(null);

        try {
            const formData = new FormData();
            formData.append('file', selectedImage);

            const response = await fetch('http://localhost:8000/classify', {
                method: 'POST',
                body: formData,
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Có lỗi xảy ra khi phân loại biển báo');
            }

            const data = await response.json();
            setClassificationResult(data);
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    const formatConfidence = (confidence) => {
        return (confidence * 100).toFixed(2) + '%';
    };

    return (
        <div className="classification-container">
            <h1>Phân loại biển báo giao thông</h1>

            <div className="upload-section">
                <ImageUploader onImageUpload={handleImageUpload} />
                {selectedImage && (
                    <button
                        className="classify-button"
                        onClick={classifySign}
                        disabled={loading}
                    >
                        {loading ? 'Đang xử lý...' : 'Phân loại biển báo'}
                    </button>
                )}
            </div>

            {error && <div className="error-message">{error}</div>}

            <div className="result-container">
                {imageUrl && (
                    <div className="image-preview">
                        <h3>Hình ảnh</h3>
                        <img
                            src={imageUrl}
                            alt="Uploaded"
                            className="uploaded-image"
                        />
                    </div>
                )}

                {classificationResult && (
                    <div className="classification-result">
                        <h3>Kết quả phân loại</h3>
                        <div className="result-card">
                            <div className="result-item">
                                <span className="result-label">Loại biển báo:</span>
                                <span className="result-value">{classificationResult.sign_name}</span>
                            </div>
                            <div className="result-item">
                                <span className="result-label">Mã biển báo:</span>
                                <span className="result-value">#{classificationResult.class_id}</span>
                            </div>
                            <div className="result-item">
                                <span className="result-label">Độ tin cậy:</span>
                                <span className="result-value confidence">
                  {formatConfidence(classificationResult.confidence)}
                </span>
                                <div className="confidence-bar">
                                    <div
                                        className="confidence-fill"
                                        style={{ width: formatConfidence(classificationResult.confidence) }}
                                    ></div>
                                </div>
                            </div>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
};

export default TrafficSignClassification;
