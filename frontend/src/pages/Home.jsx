import { useEffect, useState } from 'react';
import { getEvents } from '../services/eventService';
import { getPersons } from '../services/personService';
import { getUsers } from '../services/userService';
import { CalendarDays, UsersRound, Users } from 'lucide-react';

const Home = () => {
    const [stats, setStats] = useState({
        events: 0,
        attendees: 0,
        users: 0
    });

    useEffect(() => {
        Promise.all([
            getEvents().catch(() => []),
            getPersons().catch(() => []),
            getUsers().catch(() => [])
        ]).then(([eventsData, personsData, usersData]) => {
            setStats({
                events: eventsData.length,
                attendees: personsData.length,
                users: usersData.length
            });
        });
    }, []);

    return (
        <div>
            <div className="page-header">
                <h1 className="page-title">Dashboard Overview</h1>
            </div>

            <div className="grid grid-cols-3">
                <div className="card" style={{ borderLeft: '4px solid var(--primary-color)' }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                        <div>
                            <p className="form-label" style={{ marginBottom: 0 }}>Total Events</p>
                            <h2 style={{ fontSize: '2.5rem', fontWeight: 700 }}>{stats.events}</h2>
                        </div>
                        <div style={{ padding: '1rem', background: 'rgba(59, 130, 246, 0.1)', borderRadius: '50%' }}>
                            <CalendarDays size={32} color="var(--primary-color)" />
                        </div>
                    </div>
                </div>

                <div className="card" style={{ borderLeft: '4px solid var(--secondary-color)' }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                        <div>
                            <p className="form-label" style={{ marginBottom: 0 }}>Total Attendees</p>
                            <h2 style={{ fontSize: '2.5rem', fontWeight: 700 }}>{stats.attendees}</h2>
                        </div>
                        <div style={{ padding: '1rem', background: 'rgba(139, 92, 246, 0.1)', borderRadius: '50%' }}>
                            <UsersRound size={32} color="var(--secondary-color)" />
                        </div>
                    </div>
                </div>

                <div className="card" style={{ borderLeft: '4px solid #10b981' }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                        <div>
                            <p className="form-label" style={{ marginBottom: 0 }}>System Admins</p>
                            <h2 style={{ fontSize: '2.5rem', fontWeight: 700 }}>{stats.users}</h2>
                        </div>
                        <div style={{ padding: '1rem', background: 'rgba(16, 185, 129, 0.1)', borderRadius: '50%' }}>
                            <Users size={32} color="#10b981" />
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Home;
