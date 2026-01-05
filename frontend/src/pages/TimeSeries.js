import React, { useState, useEffect } from 'react';
import { timeSeriesAPI } from '../services/api';

const TimeSeries = () => {
  const [timeSeriesList, setTimeSeriesList] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [formData, setFormData] = useState({ name: '', description: '', dataFile: null });

  useEffect(() => {
    loadTimeSeries();
  }, []);

  const loadTimeSeries = async () => {
    try {
      const response = await timeSeriesAPI.getAll();
      setTimeSeriesList(response.data.timeSeries || []);
    } catch (error) {
      console.error('Failed to load time series:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    // For demo purposes, create sample data
    const sampleData = Array.from({ length: 100 }, (_, i) => ({
      timestamp: new Date(Date.now() - (100 - i) * 24 * 60 * 60 * 1000).toISOString(),
      value: Math.sin(i / 10) * 50 + Math.random() * 20 + 100
    }));

    try {
      await timeSeriesAPI.create({
        name: formData.name,
        description: formData.description,
        data: sampleData,
        metadata: { frequency: 'daily', units: 'units' }
      });
      
      setShowModal(false);
      setFormData({ name: '', description: '', dataFile: null });
      loadTimeSeries();
    } catch (error) {
      console.error('Failed to create time series:', error);
      alert('Failed to create time series');
    }
  };

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure you want to delete this time series?')) {
      try {
        await timeSeriesAPI.delete(id);
        loadTimeSeries();
      } catch (error) {
        console.error('Failed to delete time series:', error);
      }
    }
  };

  if (loading) {
    return <div className="text-center py-8">Loading...</div>;
  }

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold text-gray-900">Time Series Data</h1>
        <button
          onClick={() => setShowModal(true)}
          className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700"
        >
          + Upload Time Series
        </button>
      </div>

      {/* Time Series List */}
      <div className="bg-white rounded-lg shadow overflow-hidden">
        {timeSeriesList.length === 0 ? (
          <div className="text-center py-12 text-gray-500">
            No time series data yet. Upload your first dataset to get started.
          </div>
        ) : (
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Name</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Data Points</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Date Range</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Created</th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">Actions</th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {timeSeriesList.map((ts) => (
                <tr key={ts.id}>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="text-sm font-medium text-gray-900">{ts.name}</div>
                    <div className="text-sm text-gray-500">{ts.description}</div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {ts.dataPoints}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {new Date(ts.startDate).toLocaleDateString()} - {new Date(ts.endDate).toLocaleDateString()}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {new Date(ts.createdAt).toLocaleDateString()}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                    <button
                      onClick={() => handleDelete(ts.id)}
                      className="text-red-600 hover:text-red-900"
                    >
                      Delete
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>

      {/* Create Modal */}
      {showModal && (
        <div className="fixed inset-0 bg-gray-600 bg-opacity-50 flex items-center justify-center">
          <div className="bg-white rounded-lg p-8 max-w-md w-full">
            <h2 className="text-2xl font-bold mb-4">Upload Time Series</h2>
            <form onSubmit={handleSubmit}>
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-2">Name</label>
                <input
                  type="text"
                  value={formData.name}
                  onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                  required
                />
              </div>
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-2">Description</label>
                <textarea
                  value={formData.description}
                  onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                  rows={3}
                />
              </div>
              <p className="text-sm text-gray-500 mb-4">
                Demo: Sample data will be generated automatically
              </p>
              <div className="flex justify-end space-x-3">
                <button
                  type="button"
                  onClick={() => setShowModal(false)}
                  className="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
                >
                  Create
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default TimeSeries;
