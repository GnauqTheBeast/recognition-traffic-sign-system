import React from 'react';
import { useNavigate } from 'react-router-dom';
import '../styles/Home.css';

const Home = () => {
    const navigate = useNavigate();

    return (
        <div className="home-container">
            <h1>Đây là trang admin.</h1>
            <div className="button-group">
                <button onClick={() => navigate('/users')}>Quản lý User</button>
                <button onClick={() => navigate('/traffic-signs')}>Quản lý Biển báo giao thông</button>
            </div>
        </div>
    );
};

export default Home;
