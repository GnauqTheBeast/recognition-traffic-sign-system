import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import '../styles/UserList.css';

function UserList() {
    const [users, setUsers] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        setLoading(true);
        fetch('http://localhost:8080/api/users')
            .then(res => {
                if (!res.ok) {
                    throw new Error('Network response was not ok');
                }
                return res.json();
            })
            .then(data => {
                setUsers(data);
                setLoading(false);
            })
            .catch(err => {
                console.error('Error fetching users:', err);
                setError('Failed to load users. Please try again later.');
                setLoading(false);
            });
    }, []);

    const handleDelete = (id) => {
        if (window.confirm("Are you sure you want to delete this user?")) {
            setLoading(true);
            fetch(`http://localhost:8080/api/users/${id}`, {
                method: 'DELETE'
            })
            .then(res => {
                if (!res.ok) {
                    throw new Error('Failed to delete user');
                }
                setUsers(users.filter(user => user.id !== id));
                setLoading(false);
            })
            .catch(err => {
                console.error('Error deleting user:', err);
                setError('Failed to delete user. Please try again.');
                setLoading(false);
            });
        }
    };

    // Hàm để hiển thị tên đầy đủ
    const getFullName = (user) => {
        if (!user.fullName) return 'N/A';
        
        const { firstName, lastName } = user.fullName;
        
        return [firstName, lastName]
            .filter(namePart => namePart)
            .join(' ');
    };

    if (loading) {
        return <div className="loading">Loading users...</div>;
    }

    if (error) {
        return <div className="error-message">{error}</div>;
    }

    return (
        <div className="container">
            <div className="header-actions">
                <h2>User List</h2>
                <Link to="/users/new" className="add-button">Add New User</Link>
            </div>
            
            {users.length === 0 ? (
                <div className="no-users">No users found</div>
            ) : (
                <table className="user-table">
                    <thead>
                        <tr>
                            <th>Full Name</th>
                            <th>Email</th>
                            <th>Avatar</th>
                            <th>Created At</th>
                            <th>Edit</th>
                            <th>Delete</th>
                        </tr>
                    </thead>
                    <tbody>
                        {users.map(user => (
                            <tr key={user.id}>
                                <td>{getFullName(user)}</td>
                                <td>{user.email}</td>
                                <td className="avatar-cell">
                                    {user.avatarUrl ? (
                                        <img 
                                            src={user.avatarUrl} 
                                            alt="Avatar" 
                                            className="avatar-image"
                                        />
                                    ) : (
                                        <div className="no-avatar">No Avatar</div>
                                    )}
                                </td>
                                <td>
                                    {new Date(user.createdAt).toLocaleDateString()}
                                </td>
                                <td className="actions-cell">
                                    <Link to={`/admin/users/${user.id}/edit`} className="edit-button">Edit</Link>
                                </td>
                                <td>
                                    <button 
                                        onClick={() => handleDelete(user.id)} 
                                        className="delete-btn"
                                    >
                                        Delete
                                    </button>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            )}
        </div>
    );
}

export default UserList;
