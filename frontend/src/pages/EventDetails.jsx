import { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { getEventById } from '../services/eventService';
import { getAttendees, addAttendee, removeAttendee } from '../services/attendeeService';
import { getPersons } from '../services/personService';
import { UsersRound, ArrowLeft, Trash2, UserPlus } from 'lucide-react';
import Modal from '../components/Modal';

const EventDetails = () => {
    const { id } = useParams();
    const [event, setEvent] = useState(null);
    const [attendees, setAttendees] = useState([]);
    const [persons, setPersons] = useState([]);
    const [isModalOpen, setModalOpen] = useState(false);
    const [selectedPerson, setSelectedPerson] = useState('');

    const loadData = () => {
        getEventById(id).then(setEvent).catch(console.error);
        getAttendees(id).then(setAttendees).catch(console.error);
    };

    useEffect(() => {
        loadData();
    }, [id]);

    const openAddModal = () => {
        getPersons().then(data => {
            // Filter out people who are already attending
            const attendeesIds = new Set(attendees.map(a => a.id));
            setPersons(data.filter(p => !attendeesIds.has(p.id)));
            setModalOpen(true);
        }).catch(console.error);
    };

    const handleAddAttendee = async (e) => {
        e.preventDefault();
        if (!selectedPerson) return;
        try {
            await addAttendee(id, selectedPerson);
            setModalOpen(false);
            setSelectedPerson('');
            loadData();
        } catch (err) {
            console.error(err);
            alert('Error adding attendee');
        }
    };

    const handleRemoveAttendee = async (personId) => {
        try {
            await removeAttendee(id, personId);
            loadData();
        } catch (err) {
            console.error(err);
            alert('Error removing attendee');
        }
    };

    if (!event) return <div style={{ padding: '2rem' }}>Loading event details...</div>;

    return (
        <div>
            <div className="page-header" style={{ alignItems: 'flex-start', flexDirection: 'column', gap: '1rem' }}>
                <Link to="/events" style={{ display: 'inline-flex', alignItems: 'center', gap: '0.5rem', color: 'var(--text-muted)', textDecoration: 'none', transition: 'var(--transition)' }}>
                    <ArrowLeft size={16} /> Back to Events
                </Link>
                <div style={{ display: 'flex', justifyContent: 'space-between', width: '100%', alignItems: 'center' }}>
                    <div>
                        <h1 className="page-title">{event.name}</h1>
                        <p style={{ color: 'var(--text-muted)' }}>{event.date} • {event.location}</p>
                    </div>
                    <button className="btn btn-primary" onClick={openAddModal}>
                        <UserPlus size={18} /> Register Attendee
                    </button>
                </div>
            </div>

            <div className="card" style={{ marginTop: '2rem' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', marginBottom: '1.5rem', borderBottom: '1px solid var(--surface-border)', paddingBottom: '1rem' }}>
                    <UsersRound className="text-primary-color" size={24} color="var(--primary-color)" />
                    <h2 style={{ fontSize: '1.25rem', fontWeight: 600 }}>Registered Attendees ({attendees.length})</h2>
                </div>

                <div className="table-container">
                    <table className="table">
                        <thead>
                            <tr>
                                <th>ID</th>
                                <th>Name</th>
                                <th>Age</th>
                                <th style={{ textAlign: 'right' }}>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            {attendees.map(att => (
                                <tr key={att.id}>
                                    <td>{att.id}</td>
                                    <td style={{ fontWeight: 500 }}>{att.name}</td>
                                    <td>{att.age}</td>
                                    <td style={{ textAlign: 'right' }}>
                                        <button className="btn-icon" style={{ color: 'var(--danger-color)' }} onClick={() => handleRemoveAttendee(att.id)}>
                                            <Trash2 size={18} />
                                        </button>
                                    </td>
                                </tr>
                            ))}
                            {attendees.length === 0 && (
                                <tr>
                                    <td colSpan="4" style={{ textAlign: 'center', padding: '2rem', color: 'var(--text-muted)' }}>
                                        No attendees registered for this event yet.
                                    </td>
                                </tr>
                            )}
                        </tbody>
                    </table>
                </div>
            </div>

            <Modal isOpen={isModalOpen} onClose={() => setModalOpen(false)} title="Register Attendee">
                <form onSubmit={handleAddAttendee}>
                    <div className="form-group">
                        <label className="form-label">Select Person</label>
                        <select
                            className="form-control"
                            value={selectedPerson}
                            onChange={(e) => setSelectedPerson(e.target.value)}
                            required
                        >
                            <option value="" disabled>-- Select a person --</option>
                            {persons.map(p => (
                                <option key={p.id} value={p.id}>{p.name} (Age: {p.age})</option>
                            ))}
                        </select>
                    </div>
                    <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '1rem', marginTop: '2rem' }}>
                        <button type="button" className="btn" onClick={() => setModalOpen(false)}>Cancel</button>
                        <button type="submit" className="btn btn-primary" disabled={!selectedPerson}>Register</button>
                    </div>
                </form>
            </Modal>
        </div>
    );
};

export default EventDetails;
