import { useState, useEffect } from 'react';
import FullCalendar from '@fullcalendar/react';
import dayGridPlugin from '@fullcalendar/daygrid';
import timeGridPlugin from '@fullcalendar/timegrid';
import interactionPlugin from '@fullcalendar/interaction';
import { Paper, Stack, Snackbar, Alert } from '@mui/material';
import { formatDate } from '@fullcalendar/core';
import { createEvent, updateEvent, fetchEvents, deleteEvent } from './handleEvents';
import './Calendar.css';

function renderEventContent(eventInfo) {
    return (
        <>
            <b>{eventInfo.timeText}</b>
            <i>{eventInfo.event.title}</i>
        </>
    );
}

function SidebarEvent({ event }) {
    return (
        <li key={event.id}>
            <b>{formatDate(event.start, { year: 'numeric', month: 'short', day: 'numeric' })}</b>
            <i>{event.title}</i>
        </li>
    );
}

const Calendar = () => {
    const [weekendsVisible, setWeekendsVisible] = useState(true);
    const [currentEvents, setCurrentEvents] = useState([]);
    const [apiEvents, setApiEvents] = useState([]);
    const [snackbar, setSnackbar] = useState({ open: false, message: '', severity: 'success' });

    useEffect(() => {
        const loadEvents = async () => {
            const events = await fetchEvents();
            setApiEvents(events);
            setCurrentEvents(events);
        };
        loadEvents();
    }, []);

    let eventGuid = 0;
    function createEventId() {
        return String(eventGuid++);
    }

    const handleSnackbarClose = () => setSnackbar({ ...snackbar, open: false });

    function handleDateSelect(selectInfo) {
        let title = prompt('Please enter a new title for your event');
        let calendarApi = selectInfo.view.calendar;

        calendarApi.unselect();

        if (title) {
            const event = {
                id: createEventId(),
                title: title,
                date: selectInfo.startStr,
            };
            calendarApi.addEvent(event);
            setCurrentEvents([...currentEvents, event]);
            createEvent({
                id: event.id,
                title: event.title,
                date: event.date,
            });
            setApiEvents([...apiEvents, event]);
            setSnackbar({ open: true, message: 'Event created successfully!', severity: 'success' });
        }
    }

    function handleEventClick(clickInfo) {
        const action = prompt(
            `Do you want to update or delete the event '${clickInfo.event.title}'? Type 'update' or 'delete'.`
        );

        if (action) {
            if (action.toLowerCase() === 'delete') {
                if (confirm(`Are you sure you want to delete the event '${clickInfo.event.title}'`)) {
                    clickInfo.event.remove();
                    deleteEvent(clickInfo.event.id);
                    setApiEvents(apiEvents.filter((event) => event.id !== clickInfo.event.id));
                    setCurrentEvents(currentEvents.filter((event) => event.id !== clickInfo.event.id));
                    setSnackbar({ open: true, message: 'Event deleted successfully!', severity: 'success' });
                }

            } else if (action.toLowerCase() === 'update') {
                const newTitle = prompt('Please enter the new title for the event', clickInfo.event.title);

                if (newTitle) {
                    clickInfo.event.setProp('title', newTitle);

                    updateEvent({
                        id: clickInfo.event.id,
                        title: newTitle,
                        date: clickInfo.event.startStr,
                    });

                    const updatedEvents = apiEvents.map((event) =>
                        event.id === clickInfo.event.id
                            ? { ...event, title: newTitle }
                            : event
                    );

                    setApiEvents(updatedEvents);
                    setCurrentEvents(updatedEvents);

                    setSnackbar({ open: true, message: 'Event updated successfully!', severity: 'success' });
                }
            } else {
                alert('Invalid action. Please type "update" or "delete".');
            }
        }
    }

    function handleEvents(events) {
        setCurrentEvents(events);
    }

    return (
        <Stack direction={"row"}>
            <Paper className='demo-app-sidebar'>
                <h2 style={{ textAlign: "center" }}>All Events ({currentEvents.length})</h2>
                <ul>
                    {currentEvents.map((event) => (
                        <SidebarEvent key={event.id} event={event} />
                    ))}
                </ul>
            </Paper>

            <div className='demo-app-main'>
                <FullCalendar
                    plugins={[dayGridPlugin, timeGridPlugin, interactionPlugin]}
                    headerToolbar={{
                        left: 'prev,next today',
                        center: 'title',
                        right: 'dayGridMonth,timeGridWeek,timeGridDay',
                    }}
                    initialView='dayGridMonth'
                    editable={true}
                    selectable={true}
                    selectMirror={true}
                    dayMaxEvents={true}
                    weekends={weekendsVisible}
                    events={apiEvents}
                    select={handleDateSelect}
                    eventContent={renderEventContent}
                    eventClick={handleEventClick}
                    eventsSet={handleEvents}
                />
            </div>

            <Snackbar
                open={snackbar.open}
                autoHideDuration={4000}
                onClose={handleSnackbarClose}
                anchorOrigin={{ vertical: 'top', horizontal: 'right' }}
            >
                <Alert onClose={handleSnackbarClose} severity={snackbar.message.includes("successfully") ? "success" : "error"} sx={{ width: '100%' }}>
                    {snackbar.message}
                </Alert>
            </Snackbar>
        </Stack>
    );
};

export default Calendar;
