import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import '../styles/VideoDetectionHistory.css';

const VideoDetectionHistory = () => {
    const [detectionHistory, setDetectionHistory] = useState([]);

    useEffect(() => {
        const user = JSON.parse(localStorage.getItem('user'));
        const userId = user?.id;
        const key = `detectedVideoResults_${userId}`;
        const history = JSON.parse(localStorage.getItem(key)) || [];
        setDetectionHistory(history);
    }, []);

    const formatDate = (dateString) => {
        return new Date(dateString).toLocaleString('vi-VN');
    };

    return (
        <div className="history-container">
            <header className="history-header">
                <h1>Lịch sử nhận diện video</h1>
                <div className="header-actions">
                    <Link to="/vision/detect-video" className="back-link">Quay lại trang nhận diện video</Link>
                </div>
            </header>

            <div className="history-content">
                {detectionHistory.length === 0 ? (
                    <div className="no-history">
                        <p>Chưa có lịch sử nhận diện video</p>
                    </div>
                ) : (
                    <div className="history-list">
                        {detectionHistory.map((item) => (
                            <div key={item.id} className="history-item">
                                <div className="item-info">
                                    <h3>{item.originalName}</h3>
                                    <p>Thời gian: {formatDate(item.date)}</p>
                                    <p>Model sử dụng: {item.modelUsed.toUpperCase()}</p>
                                </div>
                                <div className="video-preview">
                                    <video
                                        src={item.videoPath}
                                        controls
                                        className="history-video"
                                    />
                                </div>
                            </div>
                        ))}
                    </div>
                )}
            </div>
        </div>
    );
};

export default VideoDetectionHistory; 