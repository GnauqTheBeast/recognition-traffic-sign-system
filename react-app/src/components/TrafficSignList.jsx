import React, { useState, useEffect } from 'react';
import { TrafficSignService } from '../services/trafficSignService';
import { Link } from 'react-router-dom';
import '../styles/TrafficSignList.css';

const TrafficSignList = () => {
  const [trafficSigns, setTrafficSigns] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchTrafficSigns = async () => {
      try {
        const data = await TrafficSignService.getAllTrafficSigns();
        setTrafficSigns(data);
        setLoading(false);
      } catch (err) {
        setError('Error fetching traffic signs');
        setLoading(false);
      }
    };

    fetchTrafficSigns();
  }, []);

  if (loading) return <div className="loading">Loading...</div>;
  if (error) return <div className="error">Error: {error}</div>;

  return (
    <div className="traffic-sign-container">
      <div className="header-bar">
        <h1 className="header-title">Traffic Signs Management</h1>
        <Link to="/admin/traffic-signs/new" className="add-button">
          Add New Traffic Sign
        </Link>
      </div>

      <div className="table-wrapper">
        <table className="traffic-table">
          <thead>
            <tr>
              <th>Image</th>
              <th>Name</th>
              <th>Description</th>
              <th>Type</th>
              <th>xMin</th>
              <th>yMin</th>
              <th>xMax</th>
              <th>yMax</th>
              <th>Edit</th>
              <th>Delete</th>
            </tr>
          </thead>
          <tbody>
            {trafficSigns.map((sign) => (
              <tr key={sign.id}>
                <td>
                  {sign.imageUrl ? (
                    <img
                      src={sign.imageUrl}
                      alt={sign.name}
                      className="image-thumbnail"
                    />
                  ) : (
                    <span>No image</span>
                  )}
                </td>
                <td>{sign.name}</td>
                <td>{sign.description}</td>
                <td><span className="type-tag">{sign.type}</span></td>
                <td>{sign.xMin}</td>
                <td>{sign.yMin}</td>
                <td>{sign.xMax}</td>
                <td>{sign.yMax}</td>
                <td>
                  <Link to={`/admin/traffic-signs/${sign.id}/edit`} className="btn-action edit-link">
                    Edit
                  </Link>
                </td>
                <td>
                  <div
                    className="btn-action delete-btn"
                    onClick={async () => {
                      if (window.confirm('Are you sure you want to delete this traffic sign?')) {
                        try {
                          await TrafficSignService.deleteTrafficSign(sign.id);
                          setTrafficSigns(trafficSigns.filter(s => s.id !== sign.id));
                        } catch (err) {
                          setError('Error deleting traffic sign');
                        }
                      }
                    }}
                  >
                    Delete
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default TrafficSignList;
