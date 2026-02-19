import React, { useState, useEffect } from 'react';
import { predictionsAPI, modelsAPI } from '../services/api';

const Predictions = () => {
  const [predictions, setPredictions] = useState([]);
  const [models, setModels] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [formData, setFormData] = useState({
    modelId: '',
    horizon: 10
  });

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const [predictionsRes, modelsRes] = await Promise.all([
        predictionsAPI.getAll(),
        modelsAPI.getAll()
      ]);
      
      setPredictions(predictionsRes.data.predictions || []);
      setModels(modelsRes.data.models?.filter(m => m.status === 'completed') || []);
    } catch (error) {
      console.error('Failed to load data:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    try {
      await predictionsAPI.create(formData);
      setShowModal(false);
      setFormData({ modelId: '', horizon: 10 });
      loadData();
    } catch (error) {
      console.error('Failed to create prediction:', error);
      alert('Failed to generate prediction');
    }
  };

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure you want to delete this prediction?')) {
      try {
        await predictionsAPI.delete(id);
        loadData();
      } catch (error) {
        console.error('Failed to delete prediction:', error);
      }
    }
  };

  const handleExport = async (id, format) => {
    try {
      const response = await predictionsAPI.export(id, format);
      
      const blob = response.data;
      const downloadUrl = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = downloadUrl;
      
      // Determine file extension based on format
      const fileExtensions = {
        csv: 'csv',
        xml: 'xml',
        json: 'json',
        manychat: 'json',
        botbuilders: 'json',
        openclaw: 'json',
        moltbook: 'json'
      };
      const extension = fileExtensions[format] || 'json';
      
      link.download = `prediction-${id}.${extension}`;
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(downloadUrl);
    } catch (error) {
      console.error('Failed to export prediction:', error);
      alert('Failed to export prediction');
    }
  };

  if (loading) {
    return <div className="text-center py-8">Loading...</div>;
  }

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold text-gray-900">Predictions</h1>
        <button
          onClick={() => setShowModal(true)}
          className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700"
          disabled={models.length === 0}
        >
          + Generate Prediction
        </button>
      </div>

      {models.length === 0 && (
        <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4 mb-6">
          <p className="text-yellow-800">
            You need to train a model before generating predictions.
          </p>
        </div>
      )}

      {/* Predictions List */}
      <div className="space-y-4">
        {predictions.length === 0 ? (
          <div className="bg-white rounded-lg shadow p-12 text-center text-gray-500">
            No predictions yet. Generate your first prediction to get started.
          </div>
        ) : (
          predictions.map((prediction) => (
            <div key={prediction.id} className="bg-white rounded-lg shadow p-6">
              <div className="flex justify-between items-start mb-4">
                <div>
                  <h3 className="text-lg font-semibold text-gray-900">
                    {prediction.model?.name || 'Prediction'}
                  </h3>
                  <p className="text-sm text-gray-500">
                    Model: {prediction.model?.modelType?.toUpperCase()} | 
                    Horizon: {prediction.horizon} steps | 
                    Created: {new Date(prediction.createdAt).toLocaleString()}
                  </p>
                </div>
                <div className="flex gap-2">
                  <div className="relative group">
                    <button className="bg-green-100 text-green-700 px-3 py-1 rounded text-sm hover:bg-green-200">
                      Export ▼
                    </button>
                    <div className="absolute right-0 mt-1 w-48 bg-white rounded-lg shadow-lg border hidden group-hover:block z-10">
                      <button
                        onClick={() => handleExport(prediction.id, 'json')}
                        className="block w-full text-left px-4 py-2 hover:bg-gray-100 text-sm"
                      >
                        Export as JSON
                      </button>
                      <button
                        onClick={() => handleExport(prediction.id, 'csv')}
                        className="block w-full text-left px-4 py-2 hover:bg-gray-100 text-sm"
                      >
                        Export as CSV
                      </button>
                      <button
                        onClick={() => handleExport(prediction.id, 'xml')}
                        className="block w-full text-left px-4 py-2 hover:bg-gray-100 text-sm"
                      >
                        Export as XML
                      </button>
                      <button
                        onClick={() => handleExport(prediction.id, 'manychat')}
                        className="block w-full text-left px-4 py-2 hover:bg-gray-100 text-sm"
                      >
                        ManyChat Format
                      </button>
                      <button
                        onClick={() => handleExport(prediction.id, 'botbuilders')}
                        className="block w-full text-left px-4 py-2 hover:bg-gray-100 text-sm"
                      >
                        BotBuilders Format
                      </button>
                      <button
                        onClick={() => handleExport(prediction.id, 'openclaw')}
                        className="block w-full text-left px-4 py-2 hover:bg-gray-100 text-sm"
                      >
                        OpenClaw Format
                      </button>
                      <button
                        onClick={() => handleExport(prediction.id, 'moltbook')}
                        className="block w-full text-left px-4 py-2 hover:bg-gray-100 text-sm"
                      >
                        Moltbook Format
                      </button>
                    </div>
                  </div>
                  <button
                    onClick={() => handleDelete(prediction.id)}
                    className="text-red-600 hover:text-red-900 text-sm"
                  >
                    Delete
                  </button>
                </div>
              </div>
              
              <div className="bg-gray-50 rounded p-4">
                <h4 className="text-sm font-medium text-gray-700 mb-2">Predicted Values</h4>
                <div className="flex flex-wrap gap-2">
                  {prediction.predictions?.slice(0, 10).map((value, idx) => (
                    <span key={idx} className="bg-blue-100 text-blue-800 px-2 py-1 rounded text-sm">
                      {typeof value === 'number' ? value.toFixed(2) : value}
                    </span>
                  ))}
                  {prediction.predictions?.length > 10 && (
                    <span className="text-gray-500 text-sm">
                      +{prediction.predictions.length - 10} more
                    </span>
                  )}
                </div>
              </div>
            </div>
          ))
        )}
      </div>

      {/* Create Modal */}
      {showModal && (
        <div className="fixed inset-0 bg-gray-600 bg-opacity-50 flex items-center justify-center">
          <div className="bg-white rounded-lg p-8 max-w-md w-full">
            <h2 className="text-2xl font-bold mb-4">Generate Prediction</h2>
            <form onSubmit={handleSubmit}>
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-2">Model</label>
                <select
                  value={formData.modelId}
                  onChange={(e) => setFormData({ ...formData, modelId: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                  required
                >
                  <option value="">Select a trained model</option>
                  {models.map((model) => (
                    <option key={model.id} value={model.id}>
                      {model.name} ({model.modelType})
                    </option>
                  ))}
                </select>
              </div>
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Horizon (steps ahead)
                </label>
                <input
                  type="number"
                  min="1"
                  max="100"
                  value={formData.horizon}
                  onChange={(e) => setFormData({ ...formData, horizon: parseInt(e.target.value) })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                  required
                />
              </div>
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
                  Generate
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default Predictions;
