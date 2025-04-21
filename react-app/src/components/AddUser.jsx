import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import '../styles/UserList.css';

function AddUser() {
    const [form, setForm] = useState({ name: '', email: '', avatarUrl: '' });
    const navigate = useNavigate();

    const handleChange = (e) => {
        setForm({ ...form, [e.target.name]: e.target.value });
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        fetch('http://localhost:8080/api/users', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(form)
        }).then(() => navigate('/users'));
    };

    return (
        <div className="container">
            <h2>Add User</h2>
            <form onSubmit={handleSubmit}>
                <input name="name" value={form.name} onChange={handleChange} placeholder="Name" required />
                <input name="email" value={form.email} onChange={handleChange} placeholder="Email" required />
                <input name="avatarUrl" value={form.avatarUrl} onChange={handleChange} placeholder="Avatar URL" />
                <button type="submit" className="btn">Create</button>
            </form>
        </div>
    );
}

export default AddUser;
