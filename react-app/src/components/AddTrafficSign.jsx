import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import '../styles/AddTrafficSign.css';

const AddTrafficSign = () => {
    const [formData, setFormData] = useState({
        name: '',
        description: '',
        type: '',
        imageFile: null,
        xMin: '',
        yMin: '',
        xMax: '',
        yMax: ''
    });

    const [previewUrl, setPreviewUrl] = useState('');
    const [errorMessage, setErrorMessage] = useState(null);
    const navigate = useNavigate();

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
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        try {
            const formDataToSend = new FormData();

            const data = {
                name: formData.name,
                description: formData.description,
                type: formData.type,
                xMin: parseFloat(formData.xMin),
                yMin: parseFloat(formData.yMin),
                xMax: parseFloat(formData.xMax),
                yMax: parseFloat(formData.yMax),
            };

            // formDataToSend.append("data", new Blob([JSON.stringify(data)], { type: "application/json" }));
            // formDataToSend.append(
            //     "data",
            //     new Blob([JSON.stringify(data)], { type: "application/json" }),
            //     "data.json" 
            // );
            formDataToSend.append("data", JSON.stringify(data));
            formDataToSend.append("image", formData.imageFile);

            console.log(formDataToSend);

            const response = await fetch("http://localhost:8080/api/traffic-signs", {
                method: "POST",
                body: formDataToSend
            });

            if (!response.ok) {
                const errorData = await response.json();
                console.log(errorData);
                throw new Error(errorData.message || "Failed to create traffic sign");
            }

            navigate("/admin/traffic-signs");
        } catch (error) {
            if (error.message.includes("409")) {
                setErrorMessage("The traffic sign already exists! Please choose a different one.");
            } else {
                setErrorMessage("Failed to create traffic sign. Please try again.");
            }
        }
    };

    const handleBack = () => {
        navigate(-1);
    };

    return (
        <div className="form-container">
            <h2>Add New Traffic Sign</h2>
            {errorMessage && <div className="error-popup">{errorMessage}</div>}
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
                    Image:
                    <input type="file" accept="image/*" name="imageFile" onChange={handleChange} required />
                    {/* <input type="file" onChange={e => setSelectedFile(e.target.files[0])} /> */}
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

                <button type="submit">Submit</button>
            </form>
            <button className="back-button" onClick={handleBack}>Back</button>
        </div>
    );
};

export default AddTrafficSign;
