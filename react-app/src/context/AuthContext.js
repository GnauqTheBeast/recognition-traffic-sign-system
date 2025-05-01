import React, { createContext, useState, useEffect } from 'react';

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
    const [currentUser, setCurrentUser] = useState(null);
    const [token, setToken] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const user = localStorage.getItem('user');
        const storedToken = localStorage.getItem('token');

        try {
            if (user && user !== 'undefined' && storedToken) {
                setCurrentUser(JSON.parse(user));
                setToken(storedToken);
            }
        } catch (err) {
            console.error('Lỗi parse user từ localStorage:', err);
            localStorage.removeItem('user');
            localStorage.removeItem('token');
        }

        setLoading(false);
    }, []);


    const login = (userData, userToken) => {
        localStorage.setItem('user', JSON.stringify(userData));
        localStorage.setItem('token', userToken);
        setCurrentUser(userData);
        setToken(userToken);
    };

    const logout = () => {
        localStorage.removeItem('user');
        localStorage.removeItem('token');
        setCurrentUser(null);
        setToken(null);
    };

    return (
        <AuthContext.Provider value={{ currentUser, token, login, logout, loading }}>
            {children}
        </AuthContext.Provider>
    );
};
