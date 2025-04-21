import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import '../styles/UserList.css';

function UserList() {
    const [users, setUsers] = useState([]);

    useEffect(() => {
        fetch('http://192.168.49.2:30084/api/users')
            .then(res => res.json())
            .then(data => setUsers(data))
            .catch(err => console.error('Error fetching users:', err));
    }, []);

    const handleDelete = (id) => {
        if (window.confirm("Are you sure you want to delete this user?")) {
            fetch(`http://192.168.49.2:30084/api/users/${id}`, {
                method: 'DELETE'
            }).then(() => {
                setUsers(users.filter(user => user.id !== id));
            });
        }
    };

    return (
        <div className="container">
            <h2>User List</h2>
            <table>
                <thead>
                    <tr>
                        <th>Name</th>
                        <th>Email</th>
                        <th>Avatar</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    {users.map(user => (
                        <tr key={user.id}>
                            <td>{user.name}</td>
                            <td>{user.email}</td>
                            <td>
                                {user.avatarUrl ? (
                                    <img src={user.avatarUrl} alt="Avatar" width={50} />
                                ) : 'No avatar'}
                            </td>
                            <td>
                                <Link to={`/users/${user.id}/edit`} className="btn">Edit</Link>
                                <button onClick={() => handleDelete(user.id)} className="btn delete">Delete</button>
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}

export default UserList;
