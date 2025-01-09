export async function createEvent(event) {
    const response = await fetch('http://127.0.0.1:8000/api/days_holidays', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            holiday_id: event.id,
            holiday_name: event.title,
            date: event.date,
        }),
    });

    if (response.ok) {
        console.log('Event created successfully');
    } else {
        console.error('Failed to create event');
    }
}


export async function updateEvent(event) {
    const response = await fetch(`http://127.0.0.1:8000/api/days_holidays/${event.id}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            holiday_id: event.id,
            holiday_name: event.title,
            date: null
        }),
    });

    if (response.ok) {
        console.log('Event updated successfully');
    } else {
        console.error('Failed to update event');
    }
}

export async function fetchEvents() {
    const response = await fetch('http://127.0.0.1:8000/api/days_holidays');
    if (response.ok) {
        const data = await response.json();
        return data.map(event => ({
            id: event.holiday_id,
            title: event.holiday_name,
            date: event.date,
        }));
    } else {
        console.error('Failed to fetch events');
        return [];
    }
}

export async function deleteEvent(eventId) {
    const response = await fetch(`http://127.0.0.1:8000/api/days_holidays/${eventId}`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
        },
    });

    if (response.ok) {
        console.log('Event deleted successfully');
    } else {
        console.error('Failed to delete event');
    }
}
