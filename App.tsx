import React, { useState } from 'react';
import { 
  BarChart3, 
  Calendar, 
  MessageSquare, 
  Clock, 
  Users, 
  Brain,
  Video,
  Menu,
  X
} from 'lucide-react';
import Sidebar from './components/Sidebar';
import Dashboard from './components/Dashboard';
import TaskManager from './components/TaskManager';
import TimeTracker from './components/TimeTracker';
import Meetings from './components/Meetings';
import Community from './components/Community';

function App() {
  const [currentView, setCurrentView] = useState('dashboard');
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  const renderContent = () => {
    switch (currentView) {
      case 'dashboard':
        return <Dashboard />;
      case 'tasks':
        return <TaskManager />;
      case 'time':
        return <TimeTracker />;
      case 'meetings':
        return <Meetings />;
      case 'community':
        return <Community />;
      default:
        return <Dashboard />;
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 flex">
      {/* Mobile Menu Button */}
      <button
        className="lg:hidden fixed top-4 right-4 z-50 p-2 rounded-lg bg-indigo-600 text-white"
        onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
      >
        {isMobileMenuOpen ? <X size={24} /> : <Menu size={24} />}
      </button>

      {/* Sidebar */}
      <div className={`
        ${isMobileMenuOpen ? 'translate-x-0' : '-translate-x-full'}
        lg:translate-x-0 fixed lg:static inset-y-0 left-0 z-40
        transition-transform duration-300 ease-in-out
      `}>
        <Sidebar currentView={currentView} setCurrentView={setCurrentView} />
      </div>

      {/* Main Content */}
      <div className="flex-1 p-8 lg:p-12">
        {renderContent()}
      </div>
    </div>
  );
}

export default App;