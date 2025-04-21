import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { TrafficSignService } from '../services/trafficSignService';
import '../styles/AddTrafficSign.css';

const EditTrafficSign = () => {
    const { id } = useParams();
    const navigate = useNavigate();
    const [formData, setFormData] = useState({ name: '', description: '', type: '', imageUrl: '' });
    const [previewUrl, setPreviewUrl] = useState('');

    useEffect(() => {
        const fetchData = async () => {
            const sign = await TrafficSignService.getTrafficSignById(id);
            setFormData(sign);
            setPreviewUrl(sign.imageUrl);
        };
        fetchData();
    }, [id]);

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData({ ...formData, [name]: value });
        if (name === 'imageUrl') setPreviewUrl(value);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        await TrafficSignService.updateTrafficSign(id, formData);
        navigate('/');
    };

    return (
        <div className="form-container">
            <h2>Edit Traffic Sign</h2>
            <form onSubmit={handleSubmit} className="traffic-form">
                <label>Name:<input type="text" name="name" value={formData.name} onChange={handleChange} required /></label>
                <label>Description:<textarea name="description" value={formData.description} onChange={handleChange} required /></label>
                <label>Type:<input type="text" name="type" value={formData.type} onChange={handleChange} required /></label>
                <label>Image URL:<input type="text" name="imageUrl" value={formData.imageUrl} onChange={handleChange} /></label>
                {previewUrl && <img src={previewUrl} alt="Preview" className="image-preview" />}
                <button type="submit">Update</button>
            </form>
        </div>
    );
};

export default EditTrafficSign;
