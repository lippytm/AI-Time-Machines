import React, { useState, useEffect } from 'react';
import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

const aiToolsAPI = {
  getAll: (params) => axios.get(`${API_BASE_URL}/aitools`, { 
    headers: { Authorization: `Bearer ${localStorage.getItem('token')}` },
    params
  }),
  getById: (id) => axios.get(`${API_BASE_URL}/aitools/${id}`, { 
    headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
  }),
  create: (data) => axios.post(`${API_BASE_URL}/aitools`, data, { 
    headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
  }),
  update: (id, data) => axios.put(`${API_BASE_URL}/aitools/${id}`, data, { 
    headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
  }),
  delete: (id) => axios.delete(`${API_BASE_URL}/aitools/${id}`, { 
    headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
  }),
  getCategories: () => axios.get(`${API_BASE_URL}/aitools/categories`, { 
    headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
  }),
  getTypes: () => axios.get(`${API_BASE_URL}/aitools/types`, { 
    headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
  })
};

const AITools = () => {
  const [aiTools, setAITools] = useState([]);
  const [categories, setCategories] = useState([]);
  const [toolTypes, setToolTypes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [filterCategory, setFilterCategory] = useState('');
  const [filterType, setFilterType] = useState('');
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    category: 'other',
    toolType: 'library',
    url: '',
    version: '',
    documentation: '',
    github: '',
    programmingLanguages: [],
    tags: []
  });

  useEffect(() => {
    loadAITools();
    loadCategories();
    loadToolTypes();
  }, [filterCategory, filterType]);

  const loadAITools = async () => {
    try {
      const params = {};
      if (filterCategory) params.category = filterCategory;
      if (filterType) params.toolType = filterType;
      
      const response = await aiToolsAPI.getAll(params);
      setAITools(response.data.aiTools || []);
    } catch (error) {
      console.error('Failed to load AI tools:', error);
    } finally {
      setLoading(false);
    }
  };

  const loadCategories = async () => {
    try {
      const response = await aiToolsAPI.getCategories();
      setCategories(response.data.categories || []);
    } catch (error) {
      console.error('Failed to load categories:', error);
    }
  };

  const loadToolTypes = async () => {
    try {
      const response = await aiToolsAPI.getTypes();
      setToolTypes(response.data.toolTypes || []);
    } catch (error) {
      console.error('Failed to load tool types:', error);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const submitData = {
        ...formData,
        programmingLanguages: formData.programmingLanguages.length > 0 
          ? formData.programmingLanguages 
          : [],
        tags: formData.tags.length > 0 ? formData.tags : []
      };

      await aiToolsAPI.create(submitData);
      
      setShowModal(false);
      setFormData({
        name: '',
        description: '',
        category: 'other',
        toolType: 'library',
        url: '',
        version: '',
        documentation: '',
        github: '',
        programmingLanguages: [],
        tags: []
      });
      loadAITools();
    } catch (error) {
      console.error('Failed to create AI tool:', error);
      alert('Failed to create AI tool: ' + (error.response?.data?.error?.message || error.message));
    }
  };

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure you want to delete this AI tool?')) {
      try {
        await aiToolsAPI.delete(id);
        loadAITools();
      } catch (error) {
        console.error('Failed to delete AI tool:', error);
      }
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleArrayInput = (field, value) => {
    const items = value.split(',').map(item => item.trim()).filter(item => item);
    setFormData(prev => ({ ...prev, [field]: items }));
  };

  if (loading) {
    return <div className="text-center py-8">Loading...</div>;
  }

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold text-gray-900">AI Tools & Toolkits</h1>
        <button
          onClick={() => setShowModal(true)}
          className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700"
        >
          + Add AI Tool
        </button>
      </div>

      {/* Filters */}
      <div className="mb-6 flex gap-4">
        <select
          value={filterCategory}
          onChange={(e) => setFilterCategory(e.target.value)}
          className="border border-gray-300 rounded-lg px-4 py-2"
        >
          <option value="">All Categories</option>
          {categories.map(cat => (
            <option key={cat.value} value={cat.value}>{cat.label}</option>
          ))}
        </select>

        <select
          value={filterType}
          onChange={(e) => setFilterType(e.target.value)}
          className="border border-gray-300 rounded-lg px-4 py-2"
        >
          <option value="">All Types</option>
          {toolTypes.map(type => (
            <option key={type.value} value={type.value}>{type.label}</option>
          ))}
        </select>
      </div>

      {/* AI Tools List */}
      <div className="bg-white rounded-lg shadow overflow-hidden">
        {aiTools.length === 0 ? (
          <div className="text-center py-12 text-gray-500">
            <p>No AI tools found.</p>
            <button
              onClick={() => setShowModal(true)}
              className="mt-4 text-blue-600 hover:text-blue-700"
            >
              Add your first AI tool
            </button>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Name</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Category</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Type</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Version</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Languages</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Links</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Actions</th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {aiTools.map(tool => (
                  <tr key={tool.id}>
                    <td className="px-6 py-4">
                      <div className="text-sm font-medium text-gray-900">{tool.name}</div>
                      {tool.description && (
                        <div className="text-sm text-gray-500">{tool.description.substring(0, 100)}{tool.description.length > 100 ? '...' : ''}</div>
                      )}
                    </td>
                    <td className="px-6 py-4 text-sm text-gray-500">
                      {categories.find(c => c.value === tool.category)?.label || tool.category}
                    </td>
                    <td className="px-6 py-4 text-sm text-gray-500">
                      {toolTypes.find(t => t.value === tool.toolType)?.label || tool.toolType}
                    </td>
                    <td className="px-6 py-4 text-sm text-gray-500">{tool.version || '-'}</td>
                    <td className="px-6 py-4 text-sm text-gray-500">
                      {tool.programmingLanguages?.length > 0 ? tool.programmingLanguages.join(', ') : '-'}
                    </td>
                    <td className="px-6 py-4 text-sm">
                      <div className="flex gap-2">
                        {tool.url && (
                          <a href={tool.url} target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:text-blue-700">
                            Website
                          </a>
                        )}
                        {tool.documentation && (
                          <a href={tool.documentation} target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:text-blue-700">
                            Docs
                          </a>
                        )}
                        {tool.github && (
                          <a href={tool.github} target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:text-blue-700">
                            GitHub
                          </a>
                        )}
                      </div>
                    </td>
                    <td className="px-6 py-4 text-sm">
                      <button
                        onClick={() => handleDelete(tool.id)}
                        className="text-red-600 hover:text-red-700"
                      >
                        Delete
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Modal */}
      {showModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-8 max-w-2xl w-full max-h-[90vh] overflow-y-auto">
            <h2 className="text-2xl font-bold mb-4">Add AI Tool</h2>
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
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Description</label>
                  <textarea
                    name="description"
                    value={formData.description}
                    onChange={handleInputChange}
                    rows="3"
                    className="w-full border border-gray-300 rounded-lg px-4 py-2"
                  />
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Category *</label>
                    <select
                      name="category"
                      value={formData.category}
                      onChange={handleInputChange}
                      required
                      className="w-full border border-gray-300 rounded-lg px-4 py-2"
                    >
                      {categories.map(cat => (
                        <option key={cat.value} value={cat.value}>{cat.label}</option>
                      ))}
                    </select>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Type *</label>
                    <select
                      name="toolType"
                      value={formData.toolType}
                      onChange={handleInputChange}
                      required
                      className="w-full border border-gray-300 rounded-lg px-4 py-2"
                    >
                      {toolTypes.map(type => (
                        <option key={type.value} value={type.value}>{type.label}</option>
                      ))}
                    </select>
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Website URL</label>
                  <input
                    type="url"
                    name="url"
                    value={formData.url}
                    onChange={handleInputChange}
                    className="w-full border border-gray-300 rounded-lg px-4 py-2"
                    placeholder="https://example.com"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Version</label>
                  <input
                    type="text"
                    name="version"
                    value={formData.version}
                    onChange={handleInputChange}
                    className="w-full border border-gray-300 rounded-lg px-4 py-2"
                    placeholder="1.0.0"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Documentation URL</label>
                  <input
                    type="url"
                    name="documentation"
                    value={formData.documentation}
                    onChange={handleInputChange}
                    className="w-full border border-gray-300 rounded-lg px-4 py-2"
                    placeholder="https://docs.example.com"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">GitHub URL</label>
                  <input
                    type="url"
                    name="github"
                    value={formData.github}
                    onChange={handleInputChange}
                    className="w-full border border-gray-300 rounded-lg px-4 py-2"
                    placeholder="https://github.com/username/repo"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Programming Languages (comma-separated)</label>
                  <input
                    type="text"
                    value={formData.programmingLanguages.join(', ')}
                    onChange={(e) => handleArrayInput('programmingLanguages', e.target.value)}
                    className="w-full border border-gray-300 rounded-lg px-4 py-2"
                    placeholder="Python, JavaScript, Go"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Tags (comma-separated)</label>
                  <input
                    type="text"
                    value={formData.tags.join(', ')}
                    onChange={(e) => handleArrayInput('tags', e.target.value)}
                    className="w-full border border-gray-300 rounded-lg px-4 py-2"
                    placeholder="deep-learning, tensorflow, neural-networks"
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
                  Create AI Tool
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default AITools;
