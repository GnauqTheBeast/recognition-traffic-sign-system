import React, { useState, useRef, useEffect } from 'react';
import { Link } from 'react-router-dom';
import '../styles/TrafficSignClassification.css';

const TrafficSignClassification = () => {
    const [selectedImage, setSelectedImage] = useState(null);
    const [imageUrl, setImageUrl] = useState(null);
    const [classificationResult, setClassificationResult] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [availableModels, setAvailableModels] = useState([]);
    const [selectedModel, setSelectedModel] = useState('cnn');
    const fileInputRef = useRef(null);

    // Lấy danh sách model khi component mount
    useEffect(() => {
        fetchAvailableModels();
    }, []);

    const fetchAvailableModels = async () => {
        try {
            const response = await fetch('http://localhost:8000/models');
            if (!response.ok) {
                throw new Error("Không thể lấy danh sách model");
            }
            const data = await response.json();
            setAvailableModels(data.available_models);
            setSelectedModel(data.current_model);
        } catch (err) {
            console.error("Lỗi khi lấy danh sách model:", err);
        }
    };

    const handleFileChange = (e) => {
        if (e.target.files && e.target.files.length > 0) {
            const file = e.target.files[0];
            setSelectedImage(file);
            setImageUrl(URL.createObjectURL(file));
            setClassificationResult(null);
            setError(null);
        }
    };

    // Xóa URL cũ khi component unmount để tránh memory leak
    useEffect(() => {
        return () => {
            if (imageUrl) {
                URL.revokeObjectURL(imageUrl);
            }
        };
    }, [imageUrl]);

    const handleModelChange = async (model) => {
        try {
            setLoading(true);
            const response = await fetch('http://localhost:8000/set-model', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(model)
            });
            
            if (!response.ok) {
                throw new Error("Không thể thay đổi model");
            }
            
            const data = await response.json();
            setSelectedModel(data.current_model);
            
            // Reset results when changing model
            setClassificationResult(null);
        } catch (err) {
            setError(`Lỗi khi thay đổi model: ${err.message}`);
        } finally {
            setLoading(false);
        }
    };

    const handleImageUpload = () => {
        fileInputRef.current.click();
    };

    const classifySign = async () => {
        if (!selectedImage) return;

        setLoading(true);
        setError(null);

        try {
            const formData = new FormData();
            formData.append('file', selectedImage);

            console.log(`Sử dụng model: ${selectedModel}`);
            const response = await fetch(`http://localhost:8000/classify?model_type=${selectedModel}`, {
                method: 'POST',
                body: formData,
            });

            if (!response.ok) {
                let errorMessage;
                try {
                    const errorData = await response.json();
                    errorMessage = errorData.detail || `HTTP Error: ${response.status}`;
                } catch (e) {
                    errorMessage = `HTTP Error: ${response.status}`;
                }
                throw new Error(errorMessage);
            }

            const data = await response.json();
            console.log('Classification result:', data);
            
            setClassificationResult(data);
        } catch (err) {
            console.error('Error during classification:', err);
            setError(`${err.message}`);
        } finally {
            setLoading(false);
        }
    };

    const formatConfidence = (confidence) => {
        return (confidence * 100).toFixed(2) + '%';
    };

    return (
        <div className="classification-container">
            <header className="classification-header">
                <h1>Phân loại biển báo giao thông</h1>
                <div className="header-actions">
                    <Link to="/traffic-signs" className="back-button">Quay lại danh sách</Link>
                    <Link to="/traffic-signs/detect" className="detect-link">Đến trang Nhận diện</Link>
                </div>
            </header>
            
            <div className="model-selection">
                <label>Chọn model:</label>
                <div className="model-buttons">
                    {availableModels.map(model => (
                        <button
                            key={model}
                            className={`model-button ${selectedModel === model ? 'active' : ''}`}
                            onClick={() => handleModelChange(model)}
                            disabled={loading}
                        >
                            {model.toUpperCase()}
                        </button>
                    ))}
                </div>
            </div>
            
            <div className="upload-section">
                <input 
                    type="file" 
                    accept="image/*" 
                    onChange={handleFileChange} 
                    ref={fileInputRef} 
                    style={{ display: 'none' }} 
                />
                <button 
                    className="upload-button" 
                    onClick={handleImageUpload}
                >
                    Chọn ảnh
                </button>
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

            {error && (
                <div className="error-message">
                    <strong>Lỗi:</strong> {error}
                </div>
            )}

            <div className="result-container">
                {imageUrl && (
                    <div className="image-preview">
                        <h3>Hình ảnh biển báo</h3>
                        <div className="image-frame">
                            <img 
                                src={imageUrl} 
                                alt="Uploaded" 
                                className="uploaded-image" 
                            />
                        </div>
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
                            <div className="result-item">
                                <span className="result-label">Model sử dụng:</span>
                                <span className="result-value model-name">
                                    {classificationResult.model_used.toUpperCase()}
                                </span>
                            </div>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
};

export default TrafficSignClassification;