import React, { useRef } from 'react';

const ImageUploader = ({ onImageUpload }) => {
    const fileInputRef = useRef(null);

    const handleFileChange = (e) => {
        if (e.target.files && e.target.files.length > 0) {
            const file = e.target.files[0];
            onImageUpload(file);
        }
    };

    const handleClick = () => {
        fileInputRef.current.click();
    };

    return (
        <div className="image-uploader">
            <input
                type="file"
                accept="image/*"
                onChange={handleFileChange}
                ref={fileInputRef}
                style={{ display: 'none' }}
            />
            <button
                className="upload-button"
                onClick={handleClick}
            >
                Chọn ảnh
            </button>
        </div>
    );
};

export default ImageUploader;
