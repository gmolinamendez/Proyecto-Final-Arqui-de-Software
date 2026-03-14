import api from './api';

export const getAttendees = (eventId) => api.get(`/events/${eventId}/attendees`).then(res => res.data);
export const addAttendee = (eventId, personId) => api.post(`/events/${eventId}/attendees`, { person_id: personId }).then(res => res.data);
export const removeAttendee = (eventId, personId) => api.delete(`/events/${eventId}/attendees/${personId}`).then(res => res.data);
