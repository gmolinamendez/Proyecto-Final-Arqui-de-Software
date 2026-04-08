import { useEffect, useState } from 'react';
import { getUsers, createUser, deleteUser } from '../services/userService';
import Modal from '../components/Modal';
import { Plus, Trash2, Users } from 'lucide-react';

const UsersPage = () => {
    const [users, setUsers] = useState([]);
    const [isModalOpen, setModalOpen] = useState(false);
    const [formData, setFormData] = useState({ name: '', username: '', email: '', password: '' });

    const loadUsers = () => {
        getUsers().then(setUsers).catch(console.error);
    };

    useEffect(() => {
        loadUsers();
    }, []);

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            await createUser(formData);
            setModalOpen(false);
            setFormData({ name: '', username: '', email: '', password: '' });
            loadUsers();
        } catch (err) {
            console.error(err);
            alert(err.response?.data?.error || 'Error creating user (might already exist)');
        }
    };

    const handleDelete = async (id) => {
        if (window.confirm('Are you sure you want to delete this admin user?')) {
            try {
                await deleteUser(id);
                loadUsers();
            } catch (err) {
                console.error(err);
                alert('Error deleting user');
            }
        }
    };

    return (
        <div>
            <div className="page-header">
                <h1 className="page-title">Admin Panel - Users</h1>
                <button className="btn btn-primary" onClick={() => setModalOpen(true)}>
                    <Plus size={18} /> New Admin User
                </button>
            </div>

            <div className="card">
                <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', marginBottom: '1.5rem', borderBottom: '1px solid var(--surface-border)', paddingBottom: '1rem' }}>
                    <Users className="text-primary-color" size={24} color="#10b981" />
                    <h2 style={{ fontSize: '1.25rem', fontWeight: 600 }}>System Administrators ({users.length})</h2>
                </div>

                <div className="table-container">
                    <table className="table">
                        <thead>
                            <tr>
                                <th>ID</th>
                                <th>Name</th>
                                <th>Username</th>
                                <th>Email</th>
                                <th style={{ textAlign: 'right' }}>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            {users.map(user => (
                                <tr key={user.id}>
                                    <td>{user.id}</td>
                                    <td style={{ fontWeight: 500 }}>{user.name}</td>
                                    <td>{user.username}</td>
                                    <td>{user.email}</td>
                                    <td style={{ textAlign: 'right' }}>
                                        <button className="btn-icon" style={{ color: 'var(--danger-color)' }} onClick={() => handleDelete(user.id)}>
                                            <Trash2 size={18} />
                                        </button>
                                    </td>
                                </tr>
                            ))}
                            {users.length === 0 && (
                                <tr>
                                    <td colSpan="5" style={{ textAlign: 'center', padding: '2rem', color: 'var(--text-muted)' }}>
                                        No users found!
                                    </td>
                                </tr>
                            )}
                        </tbody>
                    </table>
                </div>
            </div>

            <Modal isOpen={isModalOpen} onClose={() => setModalOpen(false)} title="Add Admin User">
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
                        <label className="form-label">Username</label>
                        <input
                            type="text"
                            className="form-control"
                            value={formData.username}
                            onChange={(e) => setFormData({ ...formData, username: e.target.value })}
                            required
                        />
                    </div>
                    <div className="form-group">
                        <label className="form-label">Email</label>
                        <input
                            type="email"
                            className="form-control"
                            value={formData.email}
                            onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                            required
                        />
                    </div>
                    <div className="form-group">
                        <label className="form-label">Password</label>
                        <input
                            type="password"
                            className="form-control"
                            value={formData.password}
                            onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                            required
                        />
                    </div>
                    <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '1rem', marginTop: '2rem' }}>
                        <button type="button" className="btn" onClick={() => setModalOpen(false)}>Cancel</button>
                        <button type="submit" className="btn btn-primary">Create User</button>
                    </div>
                </form>
            </Modal>
        </div>
    );
};

export default UsersPage;
