import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { TrafficSignService } from '../services/trafficSignService';
import '../styles/AddTrafficSign.css';

const EditTrafficSign = () => {
    const { id } = useParams();
    const navigate = useNavigate();
    const [formData, setFormData] = useState({
        name: '',
        description: '',
        type: '',
        imageFile: null,
        xMin: '',
        yMin: '',
        xMax: '',
        yMax: '',
    });

    const [previewUrl, setPreviewUrl] = useState('');
    const [errorMessage, setErrorMessage] = useState(null);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const sign = await TrafficSignService.getTrafficSignById(id);
                setFormData({ ...sign, imageFile: null }); // Reset file input
                setPreviewUrl(sign.imageUrl);
            } catch (err) {
                console.error('Error fetching traffic sign:', err);
                setErrorMessage('Failed to load traffic sign data');
            }
        };
        fetchData();
    }, [id]);

    const handleChange = (e) => {
        const { name, value, type } = e.target;

        if (type === 'file') {
            const file = e.target.files[0];
            if (file) {
                setFormData({ ...formData, imageFile: file });
                setPreviewUrl(URL.createObjectURL(file));
            }
        } else {
            setFormData({ ...formData, [name]: value });
        }
        setErrorMessage(null);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const data = {
                name: formData.name,
                description: formData.description,
                type: formData.type,
                xMin: formData.xMin,
                yMin: formData.yMin,
                xMax: formData.xMax,
                yMax: formData.yMax,
                imageFile: formData.imageFile,
            };

            await TrafficSignService.updateTrafficSign(id, data);
            navigate('/admin/traffic-signs'); // Redirect to the list of traffic signs
        } catch (err) {
            console.error('Error submitting form:', err);
            setErrorMessage(err.message || 'Failed to update traffic sign');
        }
    };

    return (
        <div className="form-container">
            <h2>Edit Traffic Sign</h2>
            {errorMessage && (
                <div className="alert alert-danger" role="alert">
                    {errorMessage}
                </div>
            )}
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
                    Upload Image:
                    <input type="file" accept="image/*" onChange={handleChange} />
                </label>
                {previewUrl && <img src={previewUrl} alt="Preview" className="image-preview" />}
                <div className="coordinates-group">
                    <label>
                        X Min:
                        <input type="number" name="xMin" value={formData.xMin} onChange={handleChange} />
                    </label>
                    <label>
                        Y Min:
                        <input type="number" name="yMin" value={formData.yMin} onChange={handleChange} />
                    </label>
                    <label>
                        X Max:
                        <input type="number" name="xMax" value={formData.xMax} onChange={handleChange} />
                    </label>
                    <label>
                        Y Max:
                        <input type="number" name="yMax" value={formData.yMax} onChange={handleChange} />
                    </label>
                </div>
                <button type="submit">Update</button>
            </form>
        </div>
    );
};

export default EditTrafficSign;
