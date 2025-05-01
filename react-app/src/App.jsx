import React from 'react';
import './styles/main.css';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import TrafficSignList from "./components/TrafficSignList";
import AddTrafficSign from './components/AddTrafficSign';
import EditTrafficSign from './components/EditTrafficSign';
import Home from './components/Home';
import UserHome from './components/UserHome';

import UserList from './components/UserList';
import AddUser from './components/AddUser';
import EditUser from './components/EditUser';
import TrafficSignDetection from './components/TrafficSignDetection';
import TrafficSignClassification from './components/TrafficSignClassification';

import DetectPage from './components/DetectPage';
import ClassifyPage from './components/ClassifyPage';

import Login from './components/Login';
import Register from './components/Register';

import PrivateRoute from './components/PrivateRoute';

function App() {
    return (
        <Router>
            <Routes>
                {/* Auth routes */}
                <Route path="/login" element={<Login />} />
                <Route path="/register" element={<Register />} />

                {/* Protected user routes */}
                <Route path="/" element={
                    <PrivateRoute>
                        <UserHome />
                    </PrivateRoute>
                } />
                <Route path="/detect" element={
                    <PrivateRoute>
                        <DetectPage />
                    </PrivateRoute>
                } />
                <Route path="/classify" element={
                    <PrivateRoute>
                        <ClassifyPage />
                    </PrivateRoute>
                } />

                {/* Protected admin routes */}
                <Route path="/admin" element={
                    <PrivateRoute>
                        <Home />
                    </PrivateRoute>
                } />
                <Route path="/admin/traffic-signs" element={
                    <PrivateRoute>
                        <TrafficSignList />
                    </PrivateRoute>
                } />
                <Route path="/admin/traffic-signs/new" element={
                    <PrivateRoute>
                        <AddTrafficSign />
                    </PrivateRoute>
                } />
                <Route path="/admin/traffic-signs/:id/edit" element={
                    <PrivateRoute>
                        <EditTrafficSign />
                    </PrivateRoute>
                } />

                <Route path="/vision/detect" element={
                    <PrivateRoute>
                        <TrafficSignDetection />
                    </PrivateRoute>
                } />
                <Route path="/vision/classify" element={
                    <PrivateRoute>
                        <TrafficSignClassification />
                    </PrivateRoute>
                } />

                <Route path="/admin/users" element={
                    <PrivateRoute>
                        <UserList />
                    </PrivateRoute>
                } />
                <Route path="/admin/users/new" element={
                    <PrivateRoute>
                        <AddUser />
                    </PrivateRoute>
                } />
                <Route path="/admin/users/:id/edit" element={
                    <PrivateRoute>
                        <EditUser />
                    </PrivateRoute>
                } />
            </Routes>
        </Router>
    );
}

export default App;
