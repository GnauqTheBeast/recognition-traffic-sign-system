import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import '../styles/UserList.css';

function AddUser() {
    const [form, setForm] = useState({
        firstName: '',
        lastName: '',
        email: '',
        avatarUrl: '',
        password: '',
    });
    const navigate = useNavigate();

    const handleChange = (e) => {
        setForm({ ...form, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        const payload = {
            fullName: {
                firstName: form.firstName,
                lastName: form.lastName
            },
            email: form.email,
            avatarUrl: form.avatarUrl,
            password: "12345678" // mặc định hoặc có thể để người dùng nhập
        };

        await fetch('http://localhost:8080/api/users/register', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        navigate('/users');
    };

    return (
        <div className="container">
            <h2>Add User</h2>
            <form onSubmit={handleSubmit}>
                <input
                    name="firstName"
                    value={form.firstName}
                    onChange={handleChange}
                    placeholder="First Name"
                    required
                />
                <input
                    name="lastName"
                    value={form.lastName}
                    onChange={handleChange}
                    placeholder="Last Name"
                    required
                />
                <input
                    name="email"
                    value={form.email}
                    onChange={handleChange}
                    placeholder="Email"
                    required
                />
                <input
                    name="avatarUrl"
                    value={form.avatarUrl}
                    onChange={handleChange}
                    placeholder="Avatar URL"
                />
                
                <input
                    name="password"
                    type="password"
                    value={form.password}
                    onChange={handleChange}
                    placeholder="Password"
                    required
                />
                <button type="submit" className="btn">Create</button>
            </form>
        </div>
    );
}

export default AddUser;
