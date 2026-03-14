import api from './api';

export const getPersons = () => api.get('/persons').then(res => res.data);
export const createPerson = (data) => api.post('/persons', data).then(res => res.data);
export const deletePerson = (id) => api.delete(`/persons/${id}`).then(res => res.data);
