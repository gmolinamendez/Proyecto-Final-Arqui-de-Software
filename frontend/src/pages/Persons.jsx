import { useEffect, useState } from 'react';
import { getPersons, createPerson, deletePerson } from '../services/personService';
import Modal from '../components/Modal';
import { Plus, Trash2, UsersRound } from 'lucide-react';

const Persons = () => {
    const [persons, setPersons] = useState([]);
    const [isModalOpen, setModalOpen] = useState(false);
    const [formData, setFormData] = useState({ name: '', age: '' });

    const loadPersons = () => {
        getPersons().then(setPersons).catch(console.error);
    };

    useEffect(() => {
        loadPersons();
    }, []);

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            await createPerson({ name: formData.name, age: parseInt(formData.age, 10) });
            setModalOpen(false);
            setFormData({ name: '', age: '' });
            loadPersons();
        } catch (err) {
            console.error(err);
            alert('Error creating person');
        }
    };

    const handleDelete = async (id) => {
        if (window.confirm('Are you sure you want to remove this person?')) {
            try {
                await deletePerson(id);
                loadPersons();
            } catch (err) {
                console.error(err);
                alert('Error deleting person');
            }
        }
    };

    return (
        <div>
            <div className="page-header">
                <h1 className="page-title">Attendees Directory</h1>
                <button className="btn btn-primary" onClick={() => setModalOpen(true)}>
                    <Plus size={18} /> New Attendee
                </button>
            </div>

            <div className="card">
                <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', marginBottom: '1.5rem', borderBottom: '1px solid var(--surface-border)', paddingBottom: '1rem' }}>
                    <UsersRound className="text-secondary-color" size={24} color="var(--secondary-color)" />
                    <h2 style={{ fontSize: '1.25rem', fontWeight: 600 }}>All Registered Persons ({persons.length})</h2>
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
                            {persons.map(person => (
                                <tr key={person.id}>
                                    <td>{person.id}</td>
                                    <td style={{ fontWeight: 500 }}>{person.name}</td>
                                    <td>{person.age}</td>
                                    <td style={{ textAlign: 'right' }}>
                                        <button className="btn-icon" style={{ color: 'var(--danger-color)' }} onClick={() => handleDelete(person.id)}>
                                            <Trash2 size={18} />
                                        </button>
                                    </td>
                                </tr>
                            ))}
                            {persons.length === 0 && (
                                <tr>
                                    <td colSpan="4" style={{ textAlign: 'center', padding: '2rem', color: 'var(--text-muted)' }}>
                                        No persons found. Create a new one!
                                    </td>
                                </tr>
                            )}
                        </tbody>
                    </table>
                </div>
            </div>

            <Modal isOpen={isModalOpen} onClose={() => setModalOpen(false)} title="Add New Person">
                <form onSubmit={handleSubmit}>
                    <div className="form-group">
                        <label className="form-label">Name</label>
                        <input
                            type="text"
                            className="form-control"
                            value={formData.name}
                            onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                            required
                        />
                    </div>
                    <div className="form-group">
                        <label className="form-label">Age</label>
                        <input
                            type="number"
                            className="form-control"
                            value={formData.age}
                            onChange={(e) => setFormData({ ...formData, age: e.target.value })}
                            required
                            min="1"
                        />
                    </div>
                    <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '1rem', marginTop: '2rem' }}>
                        <button type="button" className="btn" onClick={() => setModalOpen(false)}>Cancel</button>
                        <button type="submit" className="btn btn-primary">Create Person</button>
                    </div>
                </form>
            </Modal>
        </div>
    );
};

export default Persons;
