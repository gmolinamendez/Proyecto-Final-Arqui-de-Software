import api from './api';

export const getEvents = () => api.get('/events').then(res => res.data);
export const getEventById = (id) => api.get(`/events/${id}`).then(res => res.data);
export const createEvent = (data) => api.post('/events', data).then(res => res.data);
export const updateEvent = (id, data) => api.patch(`/events/${id}`, data).then(res => res.data);
export const deleteEvent = (id) => api.delete(`/events/${id}`).then(res => res.data);
