import React, { useState, useRef, useEffect } from 'react';
import { Link } from 'react-router-dom';
import '../styles/VideoTrafficSignDetection.css';

const VideoTrafficSignDetection = () => {
    const [selectedVideo, setSelectedVideo] = useState(null);
    const [videoUrl, setVideoUrl] = useState(null);
    const [processedVideoUrl, setProcessedVideoUrl] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [availableModels, setAvailableModels] = useState([]);
    const [selectedModel, setSelectedModel] = useState('cnn');
    const fileInputRef = useRef(null);

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
            if (!file.type.startsWith('video/')) {
                setError('Vui lòng chọn file video');
                return;
            }
            setSelectedVideo(file);
            setVideoUrl(URL.createObjectURL(file));
            setProcessedVideoUrl(null);
            setError(null);
        }
    };

    useEffect(() => {
        return () => {
            if (videoUrl) {
                URL.revokeObjectURL(videoUrl);
            }
            if (processedVideoUrl) {
                URL.revokeObjectURL(processedVideoUrl);
            }
        };
    }, [videoUrl, processedVideoUrl]);

    const handleModelChange = async (modelType) => {
        setSelectedModel(modelType);
    };

    const handleVideoUpload = () => {
        fileInputRef.current.click();
    };

    const detectSigns = async () => {
        if (!selectedVideo) return;

        setLoading(true);
        setError(null);

        try {
            const formData = new FormData();
            formData.append('file', selectedVideo);

            const response = await fetch(`http://localhost:8000/api/detect-video?model_type=${selectedModel}`, {
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

            const result = await response.json();
            
            if (!result.success) {
                throw new Error(result.error_message || 'Xử lý video thất bại');
            }

            // Construct the full URL for the video
            const fullVideoUrl = `http://localhost:8000${result.video_url}`;
            setProcessedVideoUrl(fullVideoUrl);
            
            const detectedSample = {
                id: Date.now(),
                name: result.filename,
                videoPath: fullVideoUrl,
                date: new Date().toISOString().slice(0, 19).replace('T', ' '),
                modelUsed: result.model_used,
                originalName: selectedVideo.name,
                duration: result.duration,
                frameCount: result.frame_count
            };

            const user = JSON.parse(localStorage.getItem('user'));
            const userId = user?.id;

            const key = `detectedVideoResults_${userId}`;
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

    return (
        <div className="detection-container">
            <header className="detection-header">
                <h1>Nhận diện biển báo từ video</h1>
                <div className="header-actions">
                    <Link to="/vision/detect" className="detect-link">Đến trang Nhận diện ảnh</Link>
                    <Link to="/detect-video" className="history-link">Xem lịch sử</Link>
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
                    accept="video/*"
                    onChange={handleFileChange}
                    ref={fileInputRef}
                    style={{ display: 'none' }}
                />
                <button
                    className="upload-button"
                    onClick={handleVideoUpload}
                >
                    Chọn video
                </button>
                {selectedVideo && (
                    <button
                        className="detect-button"
                        onClick={detectSigns}
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
                {videoUrl && (
                    <div className="video-preview">
                        <h3>Video gốc</h3>
                        <div className="video-frame">
                            <video
                                src={videoUrl}
                                controls
                                className="uploaded-video"
                            />
                        </div>
                    </div>
                )}

                {processedVideoUrl && (
                    <div className="video-preview">
                        <h3>Video đã xử lý</h3>
                        <div className="video-frame">
                            <video
                                src={processedVideoUrl}
                                controls
                                className="processed-video"
                            />
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
};

export default VideoTrafficSignDetection; 