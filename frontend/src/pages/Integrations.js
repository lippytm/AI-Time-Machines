import React, { useState, useEffect } from 'react';
import { integrationsAPI } from '../services/api';

const Integrations = () => {
  const [integrations, setIntegrations] = useState([]);
  const [platforms, setPlatforms] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [filterPlatform, setFilterPlatform] = useState('');
  const [formData, setFormData] = useState({
    name: '',
    platform: 'webhook',
    description: '',
    apiKey: '',
    apiSecret: '',
    webhookUrl: '',
    config: {}
  });

  useEffect(() => {
    loadIntegrations();
    loadPlatforms();
  }, [filterPlatform]);

  const loadIntegrations = async () => {
    try {
      const params = {};
      if (filterPlatform) params.platform = filterPlatform;
      
      const response = await integrationsAPI.getAll(params);
      setIntegrations(response.data.integrations || []);
    } catch (error) {
      console.error('Failed to load integrations:', error);
    } finally {
      setLoading(false);
    }
  };

  const loadPlatforms = async () => {
    try {
      const response = await integrationsAPI.getPlatforms();
      setPlatforms(response.data.platforms || []);
    } catch (error) {
      console.error('Failed to load platforms:', error);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await integrationsAPI.create(formData);
      
      setShowModal(false);
      setFormData({
        name: '',
        platform: 'webhook',
        description: '',
        apiKey: '',
        apiSecret: '',
        webhookUrl: '',
        config: {}
      });
      loadIntegrations();
    } catch (error) {
      console.error('Failed to create integration:', error);
      alert('Failed to create integration: ' + (error.response?.data?.error?.message || error.message));
    }
  };

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure you want to delete this integration?')) {
      try {
        await integrationsAPI.delete(id);
        loadIntegrations();
      } catch (error) {
        console.error('Failed to delete integration:', error);
      }
    }
  };

  const handleTest = async (id) => {
    try {
      const response = await integrationsAPI.test(id);
      alert(response.data.message);
    } catch (error) {
      console.error('Failed to test integration:', error);
      alert('Failed to test integration: ' + (error.response?.data?.error?.message || error.message));
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const getPlatformInfo = (platformValue) => {
    return platforms.find(p => p.value === platformValue) || {};
  };

  if (loading) {
    return <div className="text-center py-8">Loading...</div>;
  }

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Platform Integrations</h1>
          <p className="text-gray-600 mt-2">Connect with ChatGPT, Grok, Replit, ManyChat, BotBuilders, and more</p>
        </div>
        <div className="flex items-center gap-3">
          <a
            href="https://github.com/new"
            target="_blank"
            rel="noopener noreferrer"
            className="bg-gray-900 text-white px-4 py-2 rounded-lg hover:bg-gray-700 flex items-center gap-2"
          >
            <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true">
              <path fillRule="evenodd" d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z" clipRule="evenodd" />
            </svg>
            Create GitHub Repository
          </a>
          <button
            onClick={() => setShowModal(true)}
            className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700"
          >
            + Add Integration
          </button>
        </div>
      </div>

      {/* Filter */}
      <div className="mb-6">
        <select
          value={filterPlatform}
          onChange={(e) => setFilterPlatform(e.target.value)}
          className="border border-gray-300 rounded-lg px-4 py-2"
        >
          <option value="">All Platforms</option>
          {platforms.map(platform => (
            <option key={platform.value} value={platform.value}>{platform.label}</option>
          ))}
        </select>
      </div>

      {/* Integrations Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {integrations.length === 0 ? (
          <div className="col-span-3 text-center py-12 bg-white rounded-lg shadow">
            <p className="text-gray-500">No integrations found.</p>
            <button
              onClick={() => setShowModal(true)}
              className="mt-4 text-blue-600 hover:text-blue-700"
            >
              Add your first integration
            </button>
          </div>
        ) : (
          integrations.map(integration => {
            const platformInfo = getPlatformInfo(integration.platform);
            return (
              <div key={integration.id} className="bg-white rounded-lg shadow p-6">
                <div className="flex items-start justify-between mb-4">
                  <div>
                    <h3 className="text-lg font-semibold text-gray-900">{integration.name}</h3>
                    <p className="text-sm text-gray-500">{platformInfo.label || integration.platform}</p>
                  </div>
                  <span className={`px-2 py-1 rounded text-xs font-semibold ${
                    integration.isActive ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'
                  }`}>
                    {integration.isActive ? 'Active' : 'Inactive'}
                  </span>
                </div>

                {integration.description && (
                  <p className="text-sm text-gray-600 mb-4">{integration.description}</p>
                )}

                <div className="mb-4">
                  <p className="text-xs text-gray-500">Status: 
                    <span className={`ml-1 font-semibold ${
                      integration.syncStatus === 'success' ? 'text-green-600' : 
                      integration.syncStatus === 'failed' ? 'text-red-600' : 
                      'text-gray-600'
                    }`}>
                      {integration.syncStatus}
                    </span>
                  </p>
                  {integration.lastSyncAt && (
                    <p className="text-xs text-gray-500 mt-1">
                      Last sync: {new Date(integration.lastSyncAt).toLocaleString()}
                    </p>
                  )}
                </div>

                <div className="flex gap-2">
                  <button
                    onClick={() => handleTest(integration.id)}
                    className="flex-1 bg-blue-100 text-blue-700 px-3 py-2 rounded text-sm hover:bg-blue-200"
                  >
                    Test
                  </button>
                  <button
                    onClick={() => handleDelete(integration.id)}
                    className="flex-1 bg-red-100 text-red-700 px-3 py-2 rounded text-sm hover:bg-red-200"
                  >
                    Delete
                  </button>
                </div>
              </div>
            );
          })
        )}
      </div>

      {/* Modal */}
      {showModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-8 max-w-2xl w-full max-h-[90vh] overflow-y-auto">
            <h2 className="text-2xl font-bold mb-4">Add Integration</h2>
            <form onSubmit={handleSubmit}>
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Name *</label>
                  <input
                    type="text"
                    name="name"
                    value={formData.name}
                    onChange={handleInputChange}
                    required
                    className="w-full border border-gray-300 rounded-lg px-4 py-2"
                    placeholder="My Integration"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Platform *</label>
                  <select
                    name="platform"
                    value={formData.platform}
                    onChange={handleInputChange}
                    required
                    className="w-full border border-gray-300 rounded-lg px-4 py-2"
                  >
                    {platforms.map(platform => (
                      <option key={platform.value} value={platform.value}>
                        {platform.label}
                      </option>
                    ))}
                  </select>
                  {formData.platform && getPlatformInfo(formData.platform).description && (
                    <p className="text-sm text-gray-500 mt-1">
                      {getPlatformInfo(formData.platform).description}
                    </p>
                  )}
                  {formData.platform === 'github' && (
                    <p className="text-sm text-blue-600 mt-1">
                      Don't have a repository yet?{' '}
                      <a
                        href="https://github.com/new"
                        target="_blank"
                        rel="noopener noreferrer"
                        className="underline hover:text-blue-800"
                      >
                        Create a new GitHub repository
                      </a>
                    </p>
                  )}
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Description</label>
                  <textarea
                    name="description"
                    value={formData.description}
                    onChange={handleInputChange}
                    rows="3"
                    className="w-full border border-gray-300 rounded-lg px-4 py-2"
                    placeholder="Brief description of this integration"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">API Key</label>
                  <input
                    type="text"
                    name="apiKey"
                    value={formData.apiKey}
                    onChange={handleInputChange}
                    className="w-full border border-gray-300 rounded-lg px-4 py-2"
                    placeholder="Your API key"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">API Secret</label>
                  <input
                    type="password"
                    name="apiSecret"
                    value={formData.apiSecret}
                    onChange={handleInputChange}
                    className="w-full border border-gray-300 rounded-lg px-4 py-2"
                    placeholder="Your API secret"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Webhook URL</label>
                  <input
                    type="url"
                    name="webhookUrl"
                    value={formData.webhookUrl}
                    onChange={handleInputChange}
                    className="w-full border border-gray-300 rounded-lg px-4 py-2"
                    placeholder="https://example.com/webhook"
                  />
                </div>
              </div>

              <div className="mt-6 flex justify-end gap-4">
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
                  Create Integration
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default Integrations;
