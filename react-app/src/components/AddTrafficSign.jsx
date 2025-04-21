import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { TrafficSignService } from '../services/trafficSignService';
import '../styles/AddTrafficSign.css';

const AddTrafficSign = () => {
    const [formData, setFormData] = useState({ name: '', description: '', type: '', imageUrl: '' });
    const [previewUrl, setPreviewUrl] = useState('');
    const navigate = useNavigate();

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData({ ...formData, [name]: value });
        if (name === 'imageUrl') setPreviewUrl(value);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        await TrafficSignService.createTrafficSign(formData);
        navigate('/');
    };

    return (
        <div className="form-container">
            <h2>Add New Traffic Sign</h2>
            <form onSubmit={handleSubmit} className="traffic-form">
                <label>
                    Name:
                    <input type="text" name="name" value={formData.name} onChange={handleChange} required />
                </label>
                <label>
                    Description:
                    <textarea name="description" value={formData.description} onChange={handleChange} required />
                </label>
                <label>
                    Type:
                    <select name="type" value={formData.type} onChange={handleChange} required>
                        <option value="" disabled>Select Type</option>
                        <option value="WARNING">Warning</option>
                        <option value="PROHIBITION">Prohibition</option>
                        <option value="INFORMATION">Information</option>
                    </select>
                </label>
                <label>
                    Image URL:
                    <input type="text" name="imageUrl" value={formData.imageUrl} onChange={handleChange} />
                </label>
                {previewUrl && <img src={previewUrl} alt="Preview" className="image-preview" />}
                <button type="submit">Submit</button>
            </form>
        </div>
    );
};

export default AddTrafficSign;