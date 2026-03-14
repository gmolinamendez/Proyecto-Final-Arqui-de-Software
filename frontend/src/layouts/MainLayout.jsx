import { Outlet, NavLink } from 'react-router-dom';
import { LayoutDashboard, CalendarDays, Users, UsersRound } from 'lucide-react';

const MainLayout = () => {
    return (
        <div className="app-container">
            <aside className="sidebar">
                <div className="sidebar-logo">
                    <CalendarDays size={28} color="var(--primary-color)" />
                    <span>EventPro</span>
                </div>
                <nav className="nav-links">
                    <NavLink to="/" className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`} end>
                        <LayoutDashboard size={20} />
                        Dashboard
                    </NavLink>
                    <NavLink to="/events" className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}>
                        <CalendarDays size={20} />
                        Events
                    </NavLink>
                    <NavLink to="/attendees" className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}>
                        <UsersRound size={20} />
                        Attendees Directory
                    </NavLink>
                    <NavLink to="/users" className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}>
                        <Users size={20} />
                        Admin Panel
                    </NavLink>
                </nav>
            </aside>
            <main className="main-content">
                <Outlet />
            </main>
        </div>
    );
};

export default MainLayout;
