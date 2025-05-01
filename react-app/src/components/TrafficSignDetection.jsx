import React, { useState, useRef, useEffect } from 'react';
import { Link } from 'react-router-dom';
import '../styles/TrafficSignDetection.css';

const TrafficSignDetection = () => {
    const [selectedImage, setSelectedImage] = useState(null);
    const [imageUrl, setImageUrl] = useState(null);
    const [originalBoundingBox, setOriginalBoundingBox] = useState(null);
    const [displayBoundingBox, setDisplayBoundingBox] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [availableModels, setAvailableModels] = useState([]);
    const [selectedModel, setSelectedModel] = useState('cnn');
    const fileInputRef = useRef(null);
    const imgRef = useRef(null);
    const imageContainerRef = useRef(null);
    
    useEffect(() => {
        fetchAvailableModels();
    }, []);

    const fetchAvailableModels = async () => {
        try {
            const response = await fetch('http://localhost:8000/api/models');
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
            setOriginalBoundingBox(null);
            setDisplayBoundingBox(null);
            setError(null);
        }
    };

    useEffect(() => {
        if (imgRef.current && originalBoundingBox) {
            updateBoundingBoxDisplay();
        }
    }, [originalBoundingBox]);

    useEffect(() => {
        const handleResize = () => {
            if (originalBoundingBox) {
                updateBoundingBoxDisplay();
            }
        };

        window.addEventListener('resize', handleResize);
        return () => {
            window.removeEventListener('resize', handleResize);
        };
    }, [originalBoundingBox]);

    // Xóa URL cũ khi component unmount để tránh memory leak
    useEffect(() => {
        return () => {
            if (imageUrl) {
                URL.revokeObjectURL(imageUrl);
            }
        };
    }, [imageUrl]);

    const updateBoundingBoxDisplay = () => {
        if (!imgRef.current || !originalBoundingBox) return;

        try {
            // Lấy kích thước hiển thị thực tế của ảnh
            const displayWidth = imgRef.current.clientWidth;
            const displayHeight = imgRef.current.clientHeight;

            // Lấy kích thước thực của ảnh gốc
            const naturalWidth = imgRef.current.naturalWidth;
            const naturalHeight = imgRef.current.naturalHeight;

            // Tính toán tỷ lệ
            const scaleX = displayWidth / naturalWidth;
            const scaleY = displayHeight / naturalHeight;

            // Áp dụng tỷ lệ vào bounding box
            const scaledBox = {
                x1: originalBoundingBox.x1 * scaleX,
                y1: originalBoundingBox.y1 * scaleY,
                x2: originalBoundingBox.x2 * scaleX,
                y2: originalBoundingBox.y2 * scaleY
            };

            setDisplayBoundingBox(scaledBox);
        } catch (err) {
            console.error("Error updating bounding box:", err);
        }
    };

    const handleModelChange = async (modelType) => {
        try {
            setLoading(true);
            
            const modelData = {
                model_type: modelType  
            };
            
            console.log("Sending model data:", JSON.stringify(modelData)); // Log để debug
            
            const response = await fetch('http://localhost:8000/api/set-model', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(modelData)
            });
            
            if (!response.ok) {
                const errorData = await response.json();
                console.error("API Error:", errorData);
                throw new Error(`Không thể thay đổi model: ${JSON.stringify(errorData)}`);
            }
            
            const data = await response.json();
            console.log("Success response:", data); 
            setSelectedModel(data.current_model);
            
        } catch (err) {
            console.error("Error details:", err);
            setError(`Lỗi khi thay đổi model: ${err.message}`);
        } finally {
            setLoading(false);
        }
    };    

    const handleImageUpload = () => {
        fileInputRef.current.click();
    };

    const detectSign = async () => {
        if (!selectedImage) return;
    
        setLoading(true);
        setError(null);
    
        try {
            const formData = new FormData();
            formData.append('file', selectedImage);
    
            console.log(`Sử dụng model: ${selectedModel}`);
            const response = await fetch(`http://localhost:8000/api/detect?model_type=${selectedModel}`, {
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
            console.log('Bounding box received:', data.bounding_box);
    
            // Lưu bounding box gốc
            setOriginalBoundingBox(data.bounding_box);
    
            // Lưu kết quả detect vào localStorage theo user
            const user = JSON.parse(localStorage.getItem('user'));
            const userId = user?.id;
    
            const detectedSample = {
                id: Date.now(),
                name: `detect_${new Date().toISOString().replace(/[-:.]/g, '').slice(0, 15)}`,
                imagePath: URL.createObjectURL(selectedImage),
                date: new Date().toISOString().slice(0, 19).replace('T', ' '),
                boundingBox: data.bounding_box,
                modelUsed: selectedModel
            };
    
            const key = `detectedResults_${userId}`;
            const previous = JSON.parse(localStorage.getItem(key)) || [];
            const updated = [...previous, detectedSample];
            localStorage.setItem(key, JSON.stringify(updated));
    
        } catch (err) {
            console.error('Error during detection:', err);
            setError(`${err.message}`);
        } finally {
            setLoading(false);
        }
    };
    

    const handleImageLoad = () => {
        console.log("Image loaded successfully");
        
        // Khi ảnh tải xong, cập nhật bounding box nếu có
        if (originalBoundingBox) {
            updateBoundingBoxDisplay();
        }
    };

    const handleImageError = (e) => {
        console.error("Image failed to load:", e);
        setError("Không thể tải hình ảnh. Vui lòng thử lại với ảnh khác.");
    };

    return (
        <div className="detection-container">
            <header className="detection-header">
                <h1>Nhận diện biển báo giao thông</h1>
                <div className="header-actions">
                    {/* <Link to="/traffic-signs" className="back-button">Quay lại danh sách</Link> */}
                    <Link to="/vision/classify" className="classify-link">Đến trang Phân loại</Link>
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
                        className="detect-button" 
                        onClick={detectSign}
                        disabled={loading}
                    >
                        {loading ? 'Đang xử lý...' : 'Nhận diện biển báo'}
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
                    <div className="image-preview" ref={imageContainerRef}>
                        <h3>Hình ảnh</h3>
                        <div className="image-container">
                            <img 
                                src={imageUrl} 
                                alt="Uploaded" 
                                className="uploaded-image" 
                                ref={imgRef}
                                onLoad={handleImageLoad}
                                onError={handleImageError}
                            />
                            {displayBoundingBox && (
                                <div 
                                    className="bounding-box"
                                    style={{
                                        left: `${displayBoundingBox.x1}px`,
                                        top: `${displayBoundingBox.y1}px`,
                                        width: `${displayBoundingBox.x2 - displayBoundingBox.x1}px`,
                                        height: `${displayBoundingBox.y2 - displayBoundingBox.y1}px`,
                                    }}
                                ></div>
                            )}
                        </div>
                    </div>
                )}
                
                <div className="info-section">
                    {originalBoundingBox && (
                        <div className="detection-info">
                            <h3>Kết quả nhận diện</h3>
                            <p>Đã phát hiện biển báo tại vị trí:</p>
                            <div className="coordinates">
                                <div className="coordinate">
                                    <span>X1:</span> {Math.round(originalBoundingBox.x1)}
                                </div>
                                <div className="coordinate">
                                    <span>Y1:</span> {Math.round(originalBoundingBox.y1)}
                                </div>
                                <div className="coordinate">
                                    <span>X2:</span> {Math.round(originalBoundingBox.x2)}
                                </div>
                                <div className="coordinate">
                                    <span>Y2:</span> {Math.round(originalBoundingBox.y2)}
                                </div>
                            </div>
                            <div className="model-info">
                                <p>Model sử dụng: <strong>{selectedModel.toUpperCase()}</strong></p>
                            </div>
                            <div className="detection-tip">
                                <p>Để phân loại biển báo này, hãy chuyển đến trang <Link to="/vision/classify" className="inline-link">Phân loại biển báo</Link> và tải lên ảnh chỉ chứa biển báo.</p>
                            </div>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default TrafficSignDetection;