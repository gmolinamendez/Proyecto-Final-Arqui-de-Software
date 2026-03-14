import { useEffect, useState } from 'react';
import { getEvents, createEvent, deleteEvent } from '../services/eventService';
import Modal from '../components/Modal';
import { Plus, Trash2, ChevronRight, CalendarDays } from 'lucide-react';
import { Link } from 'react-router-dom';

const Events = () => {
    const [events, setEvents] = useState([]);
    const [isModalOpen, setModalOpen] = useState(false);
    const [formData, setFormData] = useState({ name: '', date: '', location: '' });

    const loadEvents = () => {
        getEvents().then(setEvents).catch(console.error);
    };

    useEffect(() => {
        loadEvents();
    }, []);

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            await createEvent(formData);
            setModalOpen(false);
            setFormData({ name: '', date: '', location: '' });
            loadEvents();
        } catch (err) {
            console.error(err);
            alert('Error creating event');
        }
    };

    const handleDelete = async (id) => {
        if (window.confirm('Are you sure you want to delete this event?')) {
            try {
                await deleteEvent(id);
                loadEvents();
            } catch (err) {
                console.error(err);
                alert('Error deleting event');
            }
        }
    };

    return (
        <div>
            <div className="page-header">
                <h1 className="page-title">Events Management</h1>
                <button className="btn btn-primary" onClick={() => setModalOpen(true)}>
                    <Plus size={18} /> New Event
                </button>
            </div>

            <div className="grid grid-cols-2">
                {events.map((event) => (
                    <div key={event.id} className="card" style={{ display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
                        <div>
                            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '1rem' }}>
                                <h3 style={{ fontSize: '1.25rem', fontWeight: 600 }}>{event.name}</h3>
                                <span style={{ fontSize: '0.8rem', background: 'rgba(59, 130, 246, 0.1)', color: 'var(--primary-color)', padding: '0.25rem 0.5rem', borderRadius: '4px' }}>
                                    {event.date}
                                </span>
                            </div>
                            <p style={{ color: 'var(--text-muted)', marginBottom: '1.5rem' }}>{event.location}</p>
                        </div>

                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderTop: '1px solid var(--surface-border)', paddingTop: '1rem' }}>
                            <div style={{ display: 'flex', gap: '0.5rem' }}>
                                <button className="btn-icon" style={{ color: 'var(--danger-color)' }} onClick={() => handleDelete(event.id)}>
                                    <Trash2 size={18} />
                                </button>
                            </div>
                            <Link to={`/events/${event.id}`} className="btn btn-primary" style={{ background: 'transparent', border: '1px solid var(--primary-color)', color: 'var(--primary-color)' }}>
                                View Details <ChevronRight size={18} />
                            </Link>
                        </div>
                    </div>
                ))}
                {events.length === 0 && (
                    <div style={{ gridColumn: '1 / -1', textAlign: 'center', padding: '3rem', color: 'var(--text-muted)' }}>
                        <CalendarDays size={48} style={{ opacity: 0.5, marginBottom: '1rem' }} />
                        <p>No events found. Create your first event!</p>
                    </div>
                )}
            </div>

            <Modal isOpen={isModalOpen} onClose={() => setModalOpen(false)} title="Create New Event">
                <form onSubmit={handleSubmit}>
                    <div className="form-group">
                        <label className="form-label">Event Name</label>
                        <input
                            type="text"
                            className="form-control"
                            value={formData.name}
                            onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                            required
                        />
                    </div>
                    <div className="form-group">
                        <label className="form-label">Date</label>
                        <input
                            type="date"
                            className="form-control"
                            value={formData.date}
                            onChange={(e) => setFormData({ ...formData, date: e.target.value })}
                            required
                        />
                    </div>
                    <div className="form-group">
                        <label className="form-label">Location</label>
                        <input
                            type="text"
                            className="form-control"
                            value={formData.location}
                            onChange={(e) => setFormData({ ...formData, location: e.target.value })}
                            required
                        />
                    </div>
                    <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '1rem', marginTop: '2rem' }}>
                        <button type="button" className="btn" onClick={() => setModalOpen(false)}>Cancel</button>
                        <button type="submit" className="btn btn-primary">Create Event</button>
                    </div>
                </form>
            </Modal>
        </div>
    );
};

export default Events;
