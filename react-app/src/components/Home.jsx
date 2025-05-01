import React from 'react';
import { useNavigate } from 'react-router-dom';
import '../styles/Home.css';

const Home = () => {
    const navigate = useNavigate();

    return (
        <div className="home-container">
            <h1>Traffic Sign Vision System - Admin Page</h1>
            <div className="button-group">
                <button onClick={() => navigate('/admin/users')}>User Management</button>
                <button onClick={() => navigate('/admin/traffic-signs')}>Traffic Sign Management</button>
            </div>
        </div>
    );
};

export default Home;
