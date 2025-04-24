const API_BASE_URL = 'http://localhost:8080/api/traffic-signs';

const ALLOWED_TYPES = ['WARNING', 'PROHIBITION', 'INFORMATION'];

const normalizeTrafficSignType = (type) => type.trim().toUpperCase();

const validateTrafficSign = (trafficSign) => {
    const { name, description, imageUrl, type, xMin, yMin, xMax, yMax } = trafficSign;

    if (!name || !description || !imageUrl || !type) {
        throw new Error('All fields are required');
    }

    const normalizedType = normalizeTrafficSignType(type);
    if (!ALLOWED_TYPES.includes(normalizedType)) {
        throw new Error(`Invalid traffic sign type. Allowed types: ${ALLOWED_TYPES.join(', ')}`);
    }

    const parsedXMin = parseFloat(xMin);
    const parsedYMin = parseFloat(yMin);
    const parsedXMax = parseFloat(xMax);
    const parsedYMax = parseFloat(yMax);

    if (
        isNaN(parsedXMin) || isNaN(parsedXMax) ||
        isNaN(parsedYMin) || isNaN(parsedYMax)
    ) {
        throw new Error('Coordinates (xMin, yMin, xMax, yMax) must be valid numbers');
    }

    if (parsedXMin > parsedXMax) {
        throw new Error('xMin must be less than or equal to xMax');
    }

    if (parsedYMin > parsedYMax) {
        throw new Error('yMin must be less than or equal to yMax');
    }

    return {
        ...trafficSign,
        type: normalizedType,
        xMin: parsedXMin,
        yMin: parsedYMin,
        xMax: parsedXMax,
        yMax: parsedYMax,
    };
};

export const TrafficSignService = {
    getAllTrafficSigns: () => {
        return fetch(API_BASE_URL)
            .then(res => res.json())
            .catch(err => {
                console.error('Error fetching traffic signs:', err);
                throw new Error('Failed to fetch traffic signs');
            });
    },

    getTrafficSignById: (id) => {
        return fetch(`${API_BASE_URL}/${id}`)
            .then(res => res.json())
            .catch(err => {
                console.error('Error fetching traffic sign by id:', err);
                throw new Error('Failed to fetch traffic sign');
            });
    },

    createTrafficSign: (trafficSign) => {
        const payload = validateTrafficSign(trafficSign);
        return fetch(API_BASE_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
            },
            body: JSON.stringify(payload),
        })
            .then(res => {
                if (!res.ok) {
                    return res.json().then(errorData => {
                        console.error('Error response:', errorData);
                        throw new Error(errorData.message || 'Failed to create traffic sign');
                    });
                }
                return res.json();
            })
            .catch(err => {
                console.error('Error creating traffic sign:', err);
                throw err;
            });
    },

    updateTrafficSign: (id, trafficSign) => {
        const payload = validateTrafficSign(trafficSign);
        return fetch(`${API_BASE_URL}/${id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
            },
            body: JSON.stringify(payload),
        })
            .then(res => {
                if (!res.ok) {
                    return res.json().then(errorData => {
                        console.error('Error response:', errorData);
                        if (res.status === 409) {
                            throw new Error('Name already exists');
                        }
                        throw new Error(errorData.message || 'Failed to update traffic sign');
                    });
                }
                return res.json();
            })
            .catch(err => {
                console.error('Error updating traffic sign:', err);
                throw err;
            });
    },

    deleteTrafficSign: (id) => {
        return fetch(`${API_BASE_URL}/${id}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
            },
        })
            .then(res => {
                if (!res.ok) {
                    return res.json().then(errorData => {
                        console.error('Error response:', errorData);
                        throw new Error(errorData.message || 'Failed to delete traffic sign');
                    });
                }
            })
            .catch(err => {
                console.error('Error deleting traffic sign:', err);
                throw err;
            });
    },
};
