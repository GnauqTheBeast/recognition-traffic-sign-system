import React from 'react';
import { useNavigate } from 'react-router-dom';
import '../styles/Home.css';
import { Button } from '@mui/material';
import VideoCameraFrontIcon from '@mui/icons-material/VideoCameraFront';

function UserHome() {
    const navigate = useNavigate();

    return (
        <div className="home-container">
            <h1>Welcome to Traffic Sign System</h1>
            <div className="button-group">
                <button onClick={() => navigate('/detect')} style={{ marginRight: '10px' }}>Detect</button>
                <button onClick={() => navigate('/detect-video')}>Video Detection</button>
                <button onClick={() => navigate('/classify')}>Classify</button>
                <Button
                    variant="contained"
                    color="primary"
                    startIcon={<VideoCameraFrontIcon />}
                    onClick={() => navigate('/rtsp-stream')}
                    sx={{ m: 1 }}
                >
                    RTSP Stream
                </Button>
            </div>
        </div>
    );
}

export default UserHome;
