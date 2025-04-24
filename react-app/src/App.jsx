import React from 'react';
import './styles/main.css';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import TrafficSignList from "./components/TrafficSignList";
import AddTrafficSign from './components/AddTrafficSign';
import EditTrafficSign from './components/EditTrafficSign';
import Home from './components/Home';

import UserList from './components/UserList';
import AddUser from './components/AddUser';
import EditUser from './components/EditUser';
import TrafficSignDetection from './components/TrafficSignDetection';
import TrafficSignClassification from './components/TrafficSignClassification';

function App() {
    return (
        <Router>
            <Routes>
                {/* <Route path="/login" element={<Login />} />
                <Route path="/register" element={<Register />} /> */}

                <Route path="/" element={<Home />} />

                {/* Traffic sign routes */}
                <Route path="/traffic-signs" element={<TrafficSignList />} />
                <Route path="/traffic-signs/new" element={<AddTrafficSign />} />
                <Route path="/traffic-signs/:id/edit" element={<EditTrafficSign />} />
                <Route path="/traffic-signs/detect" element={<TrafficSignDetection />} />
                <Route path="/traffic-signs/classify" element={<TrafficSignClassification />} />

                {/* User routes */}
                <Route path="/users" element={<UserList />} />
                <Route path="/users/new" element={<AddUser />} />
                <Route path="/users/:id/edit" element={<EditUser />} />
            </Routes>
        </Router>
    );
}

export default App;
