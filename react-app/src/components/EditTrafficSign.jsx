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
        imageUrl: '',
        xMin: '',
        yMin: '',
        xMax: '',
        yMax: ''
    });

    const [previewUrl, setPreviewUrl] = useState('');
    const [imageFile, setImageFile] = useState(null);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const sign = await TrafficSignService.getTrafficSignById(id);
                setFormData(sign);
                setPreviewUrl(sign.imageUrl);
            } catch (err) {
                console.error('Error fetching traffic sign:', err);
                setError('Failed to load traffic sign data');
            }
        };
        fetchData();
    }, [id]);

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData({ ...formData, [name]: value });
        setError(null);
    };

    const handleFileChange = (e) => {
        const file = e.target.files[0];
        if (file) {
            setImageFile(file);
            setPreviewUrl(URL.createObjectURL(file));
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            let imageUrl = formData.imageUrl;

            // Nếu có file mới thì upload
            if (imageFile) {
                const uploadData = new FormData();
                uploadData.append('file', imageFile);

                const response = await TrafficSignService.uploadImage(uploadData);
                imageUrl = response.url; // Đảm bảo API trả về { url: '...' }
            }

            const updatedData = { ...formData, imageUrl };
            await TrafficSignService.updateTrafficSign(id, updatedData);
            navigate('/traffic-signs');
        } catch (err) {
            console.error('Error submitting form:', err);
            setError(err.message || 'Failed to update traffic sign');
        }
    };

    return (
        <div className="form-container">
            <h2>Edit Traffic Sign</h2>
            {error && (
                <div className="alert alert-danger" role="alert">
                    {error}
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
                    <input type="text" name="type" value={formData.type} onChange={handleChange} required />
                </label>
                <label>
                    Upload Image:
                    <input type="file" accept="image/*" onChange={handleFileChange} />
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
