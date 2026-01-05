import React, { useState, useEffect } from 'react';
import { timeSeriesAPI, modelsAPI, predictionsAPI } from '../services/api';

const Dashboard = () => {
  const [stats, setStats] = useState({
    timeSeriesCount: 0,
    modelsCount: 0,
    predictionsCount: 0
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadStats();
  }, []);

  const loadStats = async () => {
    try {
      const [timeSeriesRes, modelsRes, predictionsRes] = await Promise.all([
        timeSeriesAPI.getAll(),
        modelsAPI.getAll(),
        predictionsAPI.getAll()
      ]);

      setStats({
        timeSeriesCount: timeSeriesRes.data.count || 0,
        modelsCount: modelsRes.data.count || 0,
        predictionsCount: predictionsRes.data.count || 0
      });
    } catch (error) {
      console.error('Failed to load stats:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="text-xl text-gray-600">Loading...</div>
      </div>
    );
  }

  return (
    <div>
      <h1 className="text-3xl font-bold text-gray-900 mb-8">Dashboard</h1>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600 mb-1">Time Series</p>
              <p className="text-3xl font-bold text-blue-600">{stats.timeSeriesCount}</p>
            </div>
            <div className="bg-blue-100 p-3 rounded-full">
              <svg className="w-8 h-8 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 12l3-3 3 3 4-4M8 21l4-4 4 4M3 4h18M4 4h16v12a1 1 0 01-1 1H5a1 1 0 01-1-1V4z" />
              </svg>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600 mb-1">AI Models</p>
              <p className="text-3xl font-bold text-purple-600">{stats.modelsCount}</p>
            </div>
            <div className="bg-purple-100 p-3 rounded-full">
              <svg className="w-8 h-8 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
              </svg>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600 mb-1">Predictions</p>
              <p className="text-3xl font-bold text-green-600">{stats.predictionsCount}</p>
            </div>
            <div className="bg-green-100 p-3 rounded-full">
              <svg className="w-8 h-8 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
              </svg>
            </div>
          </div>
        </div>
      </div>

      {/* Welcome Section */}
      <div className="bg-white rounded-lg shadow p-8">
        <h2 className="text-2xl font-semibold mb-4">Welcome to AI Time Machines</h2>
        <p className="text-gray-600 mb-4">
          Your platform for creating and managing time-series AI agents. Get started by:
        </p>
        <ul className="list-disc list-inside space-y-2 text-gray-700">
          <li>Uploading time-series data in the <strong>Time Series</strong> section</li>
          <li>Training AI models with different algorithms in the <strong>Models</strong> section</li>
          <li>Generating predictions using your trained models in the <strong>Predictions</strong> section</li>
        </ul>
      </div>
    </div>
  );
};

export default Dashboard;
