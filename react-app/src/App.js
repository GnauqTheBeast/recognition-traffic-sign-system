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

function App() {
    return (
        <Router>
            <Routes>
                {/* Home page */}
                <Route path="/" element={<Home />} />

                {/* Traffic sign routes */}
                <Route path="/traffic-signs" element={<TrafficSignList />} />
                <Route path="/traffic-signs/new" element={<AddTrafficSign />} />
                <Route path="/traffic-signs/:id/edit" element={<EditTrafficSign />} />

                {/* User routes */}
                <Route path="/users" element={<UserList />} />
                <Route path="/users/new" element={<AddUser />} />
                <Route path="/users/:id/edit" element={<EditUser />} />
            </Routes>
        </Router>
    );
}

export default App;
