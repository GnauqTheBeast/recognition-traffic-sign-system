import React from 'react';
import { useNavigate } from 'react-router-dom';
import '../styles/Home.css';

function UserHome() {
    const navigate = useNavigate();

    return (
        <div className="home-container">
            <h1>Welcome to Traffic Sign System</h1>
            <div className="button-group">
                <button onClick={() => navigate('/detect')} style={{ marginRight: '10px' }}>Detect</button>
                <button onClick={() => navigate('/classify')}>Classify</button>
            </div>
        </div>
    );
}

export default UserHome;
