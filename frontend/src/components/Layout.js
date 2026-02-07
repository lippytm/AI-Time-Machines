import React from 'react';
import { Outlet, Link, useLocation } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

const Layout = () => {
  const { user, logout } = useAuth();
  const location = useLocation();

  const isActive = (path) => {
    return location.pathname === path ? 'bg-blue-700' : 'hover:bg-blue-600';
  };

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Navigation */}
      <nav className="bg-blue-600 text-white shadow-lg">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <h1 className="text-2xl font-bold">AI Time Machines</h1>
              <div className="ml-10 flex space-x-4">
                <Link
                  to="/"
                  className={`px-3 py-2 rounded-md text-sm font-medium ${isActive('/')}`}
                >
                  Dashboard
                </Link>
                <Link
                  to="/timeseries"
                  className={`px-3 py-2 rounded-md text-sm font-medium ${isActive('/timeseries')}`}
                >
                  Time Series
                </Link>
                <Link
                  to="/models"
                  className={`px-3 py-2 rounded-md text-sm font-medium ${isActive('/models')}`}
                >
                  Models
                </Link>
                <Link
                  to="/predictions"
                  className={`px-3 py-2 rounded-md text-sm font-medium ${isActive('/predictions')}`}
                >
                  Predictions
                </Link>
                <Link
                  to="/aitools"
                  className={`px-3 py-2 rounded-md text-sm font-medium ${isActive('/aitools')}`}
                >
                  AI Tools
                </Link>
                <Link
                  to="/integrations"
                  className={`px-3 py-2 rounded-md text-sm font-medium ${isActive('/integrations')}`}
                >
                  Integrations
                </Link>
              </div>
            </div>
            
            <div className="flex items-center space-x-4">
              <span className="text-sm">{user?.username}</span>
              <button
                onClick={logout}
                className="bg-blue-700 hover:bg-blue-800 px-4 py-2 rounded-md text-sm font-medium"
              >
                Logout
              </button>
            </div>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <Outlet />
      </main>
    </div>
  );
};

export default Layout;
