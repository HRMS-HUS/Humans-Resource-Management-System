import axios from 'axios';

export async function createEvent(event, token) {
    if (!event || !token) return;
    try {
        const response = await axios.post('http://52.184.86.56:8000/api/admin/holiday', null, {
            headers: {
                Authorization: `Bearer ${token}`,
            },
            params: {
                holiday_name: event.title,
                holiday_date: event.date,
            },
        });
        console.log('Event created successfully', response.data);
        return response.data;
    } catch (error) {
        console.error('Failed to create event', error);
        throw error;
    }
}

export async function updateEvent(event, token) {
    if (!event || !token) return;
    try {
        const response = await axios.put(`http://52.184.86.56:8000/api/admin/holiday/${event.id}`, null, {
            headers: {
                Authorization: `Bearer ${token}`,
            },
            params: {
                holiday_name: event.title,
                holiday_date: event.date,
            },
        });
        console.log('Event updated successfully', response.data);
        return response.data;
    } catch (error) {
        console.error('Failed to update event', error);
        throw error;
    }
}

export async function fetchEvents(token) {
    if (!token) return [];
    try {
        const response = await axios.get('http://52.184.86.56:8000/api/admin/holidays', {
            headers: {
                Authorization: `Bearer ${token}`,
            },
        });
        return response.data.map(event => ({
            id: event.holiday_id,
            title: event.holiday_name,
            date: event.holiday_date,
        }));
    } catch (error) {
        console.error('Failed to fetch events', error);
        return [];
    }
}

export async function deleteEvent(eventId, token) {
    if (!eventId || !token) return;
    try {
        const response = await axios.delete(`http://52.184.86.56:8000/api/admin/holiday/${eventId}`, {
            headers: {
                Authorization: `Bearer ${token}`,
            },
        });
        console.log('Event deleted successfully', response.data);
    } catch (error) {
        console.error('Failed to delete event', error);
        throw error;
    }
}
