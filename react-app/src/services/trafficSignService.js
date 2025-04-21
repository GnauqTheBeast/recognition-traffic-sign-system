// const API_BASE_URL = 'http://localhost:8080/api/traffic-signs';

const API_BASE_URL = 'http://192.168.49.2:30083/api/traffic-signs';


const defaultHeaders = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
};

const normalizeTrafficSignType = (type) => {
    return type.toUpperCase();
};

export const TrafficSignService = {
    getAllTrafficSigns: async () => {
        const response = await fetch(API_BASE_URL, {
            method: 'GET',
            headers: defaultHeaders,
            credentials: 'include',
        });
        if (!response.ok) {
            throw new Error('Failed to fetch traffic signs');
        }
        return response.json();
    },

    getTrafficSignById: async (id) => {
        const response = await fetch(`${API_BASE_URL}/${id}`, {
            method: 'GET',
            headers: defaultHeaders,
            credentials: 'include',
        });
        if (!response.ok) {
            throw new Error('Failed to fetch traffic sign');
        }
        return response.json();
    },

    createTrafficSign: async (trafficSign) => {
        if (
            !trafficSign.name ||
            !trafficSign.description ||
            !trafficSign.imageUrl ||
            !trafficSign.type
        ) {
            throw new Error('All fields are required');
        }

        const normalizedType = normalizeTrafficSignType(trafficSign.type);
        if (!['WARNING', 'PROHIBITION', 'INFORMATION'].includes(normalizedType)) {
            throw new Error('Invalid traffic sign type');
        }

        const payload = {
            ...trafficSign,
            type: normalizedType,
        };

        console.log('Creating traffic sign with data:', JSON.stringify(payload, null, 2));

        try {
            const response = await fetch(API_BASE_URL, {
                method: 'POST',
                headers: defaultHeaders,
                credentials: 'include',
                body: JSON.stringify(payload),
            });

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                console.error('Error response:', {
                    status: response.status,
                    statusText: response.statusText,
                    data: errorData,
                    requestBody: payload,
                });
                throw new Error(
                    errorData.message || `Failed to create traffic sign: ${response.status} ${response.statusText}`
                );
            }

            const result = await response.json();
            console.log('Create response:', result);
            return result;
        } catch (error) {
            console.error('Error in createTrafficSign:', error);
            throw error;
        }
    },

    updateTrafficSign: async (id, trafficSign) => {
        const normalizedType = normalizeTrafficSignType(trafficSign.type);
        const payload = {
            ...trafficSign,
            type: normalizedType,
        };

        console.log('Updating traffic sign with data:', payload);

        try {
            const response = await fetch(`${API_BASE_URL}/${id}`, {
                method: 'PUT',
                headers: defaultHeaders,
                credentials: 'include',
                body: JSON.stringify(payload),
            });

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                console.error('Error response:', {
                    status: response.status,
                    statusText: response.statusText,
                    data: errorData,
                });
                throw new Error(
                    errorData.message || `Failed to update traffic sign: ${response.status} ${response.statusText}`
                );
            }

            const result = await response.json();
            console.log('Update response:', result);
            return result;
        } catch (error) {
            console.error('Error in updateTrafficSign:', error);
            throw error;
        }
    },

    deleteTrafficSign: async (id) => {
        console.log('Deleting traffic sign with id:', id);

        try {
            const response = await fetch(`${API_BASE_URL}/${id}`, {
                method: 'DELETE',
                headers: defaultHeaders,
                credentials: 'include',
            });

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                console.error('Error response:', {
                    status: response.status,
                    statusText: response.statusText,
                    data: errorData,
                });
                throw new Error(
                    errorData.message || `Failed to delete traffic sign: ${response.status} ${response.statusText}`
                );
            }
        } catch (error) {
            console.error('Error in deleteTrafficSign:', error);
            throw error;
        }
    },
};
