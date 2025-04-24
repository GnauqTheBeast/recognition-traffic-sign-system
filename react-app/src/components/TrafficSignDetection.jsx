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
    const fileInputRef = useRef(null);
    const imgRef = useRef(null);
    const imageContainerRef = useRef(null);

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

    // Theo dõi thay đổi kích thước ảnh để cập nhật bounding box
    useEffect(() => {
        if (imgRef.current && originalBoundingBox) {
            updateBoundingBoxDisplay();
        }
    }, [originalBoundingBox]);

    // Thêm listener để cập nhật bounding box khi cửa sổ thay đổi kích thước
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
        if (!imgRef.current || !originalBoundingBox || !imageContainerRef.current) return;

        try {
            const containerWidth = imageContainerRef.current.clientWidth;
            const containerHeight = imageContainerRef.current.clientHeight;

            const naturalWidth = imgRef.current.naturalWidth;
            const naturalHeight = imgRef.current.naturalHeight;

            console.log("Container dimensions:", { width: containerWidth, height: containerHeight });
            console.log("Image dimensions:", { width: naturalWidth, height: naturalHeight });

            const scaleX = containerWidth / naturalWidth;
            const scaleY = containerHeight / naturalHeight;

            const scaledBox = {
                x1: originalBoundingBox.x1 * scaleX,
                y1: originalBoundingBox.y1 * scaleY,
                x2: originalBoundingBox.x2 * scaleX,
                y2: originalBoundingBox.y2 * scaleY
            };

            console.log("Original box:", originalBoundingBox);
            console.log("Scaled box:", scaledBox);

            setDisplayBoundingBox(scaledBox);
        } catch (err) {
            console.error("Error updating bounding box:", err);
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

            console.log('Sending request to detect endpoint...');
            const response = await fetch('http://localhost:8000/detect', {
                method: 'POST',
                body: formData,
            });

            console.log('Response received:', response.status);
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
                    <Link to="/traffic-signs" className="back-button">Quay lại danh sách</Link>
                    <Link to="/traffic-signs/classify" className="classify-link">Đến trang Phân loại</Link>
                </div>
            </header>

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
                            <div className="detection-tip">
                                <p>Để phân loại biển báo này, hãy chuyển đến trang <Link to="/traffic-signs/classify" className="inline-link">Phân loại biển báo</Link> và tải lên ảnh chỉ chứa biển báo.</p>
                            </div>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default TrafficSignDetection;
