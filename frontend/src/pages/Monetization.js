import React, { useState, useEffect } from 'react';
import { monetizationAPI } from '../services/api';

const Monetization = () => {
  const [plans, setPlans] = useState([]);
  const [opportunities, setOpportunities] = useState([]);
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('plans');

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const [plansRes, opportunitiesRes, summaryRes] = await Promise.all([
        monetizationAPI.getPlans(),
        monetizationAPI.getOpportunities(),
        monetizationAPI.getRevenueSummary()
      ]);
      setPlans(plansRes.data.plans || []);
      setOpportunities(opportunitiesRes.data.opportunities || []);
      setSummary(summaryRes.data.summary || null);
    } catch (error) {
      console.error('Failed to load monetization data:', error);
    } finally {
      setLoading(false);
    }
  };

  const platformColors = {
    chatgpt: 'bg-green-100 text-green-800 border-green-200',
    grok: 'bg-purple-100 text-purple-800 border-purple-200',
    replit: 'bg-orange-100 text-orange-800 border-orange-200',
    manychat: 'bg-blue-100 text-blue-800 border-blue-200',
    botbuilders: 'bg-indigo-100 text-indigo-800 border-indigo-200'
  };

  const platformIcons = {
    chatgpt: '🤖',
    grok: '⚡',
    replit: '💻',
    manychat: '💬',
    botbuilders: '🔧'
  };

  if (loading) {
    return <div className="text-center py-8">Loading...</div>;
  }

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Monetization</h1>
        <p className="text-gray-600 mt-2">
          Turn your AI predictions into revenue with ChatGPT, Grok, Replit, ManyChat, and BotBuilders.
        </p>
      </div>

      {/* Revenue Summary Card */}
      {summary && (
        <div className="bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg p-6 text-white mb-8">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-blue-100 text-sm font-medium uppercase tracking-wide">Current Plan</p>
              <p className="text-3xl font-bold capitalize mt-1">{summary.currentPlan}</p>
              <p className="text-blue-100 mt-2">{summary.message}</p>
            </div>
            <div className="text-right">
              <p className="text-blue-100 text-sm">Estimated Monthly Revenue</p>
              <p className="text-4xl font-bold">${summary.estimatedMonthlyRevenue}</p>
              <p className="text-blue-100 text-sm mt-1">{summary.currency}/month</p>
            </div>
          </div>
        </div>
      )}

      {/* Tabs */}
      <div className="border-b border-gray-200 mb-6">
        <nav className="-mb-px flex space-x-8">
          <button
            onClick={() => setActiveTab('plans')}
            className={`py-2 px-1 border-b-2 font-medium text-sm ${
              activeTab === 'plans'
                ? 'border-blue-500 text-blue-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            }`}
          >
            Subscription Plans
          </button>
          <button
            onClick={() => setActiveTab('opportunities')}
            className={`py-2 px-1 border-b-2 font-medium text-sm ${
              activeTab === 'opportunities'
                ? 'border-blue-500 text-blue-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            }`}
          >
            Revenue Opportunities
          </button>
        </nav>
      </div>

      {/* Subscription Plans Tab */}
      {activeTab === 'plans' && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {plans.map((plan) => (
            <div
              key={plan.id}
              className={`bg-white rounded-lg shadow-lg p-6 flex flex-col ${
                plan.highlighted ? 'ring-2 ring-blue-500 relative' : ''
              }`}
            >
              {plan.highlighted && (
                <div className="absolute -top-3 left-1/2 transform -translate-x-1/2">
                  <span className="bg-blue-500 text-white text-xs font-semibold px-3 py-1 rounded-full">
                    MOST POPULAR
                  </span>
                </div>
              )}
              <div className="mb-4">
                <h3 className="text-xl font-bold text-gray-900">{plan.name}</h3>
                <p className="text-gray-500 text-sm mt-1">{plan.description}</p>
              </div>
              <div className="mb-6">
                <span className="text-4xl font-bold text-gray-900">${plan.price}</span>
                <span className="text-gray-500">/{plan.interval}</span>
              </div>
              <ul className="space-y-2 flex-1 mb-6">
                {plan.features.map((feature, index) => (
                  <li key={index} className="flex items-start text-sm text-gray-600">
                    <span className="text-green-500 mr-2 mt-0.5 flex-shrink-0">✓</span>
                    {feature}
                  </li>
                ))}
              </ul>
              <button
                className={`w-full py-2 px-4 rounded-lg font-medium text-sm transition-colors ${
                  plan.highlighted
                    ? 'bg-blue-600 text-white hover:bg-blue-700'
                    : plan.price === 0
                    ? 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                    : 'bg-gray-900 text-white hover:bg-gray-800'
                }`}
              >
                {plan.price === 0 ? 'Current Plan' : `Upgrade to ${plan.name}`}
              </button>
            </div>
          ))}
        </div>
      )}

      {/* Revenue Opportunities Tab */}
      {activeTab === 'opportunities' && (
        <div className="space-y-6">
          {opportunities.map((opp) => (
            <div key={opp.platform} className="bg-white rounded-lg shadow p-6">
              <div className="flex items-start justify-between mb-4">
                <div className="flex items-center gap-3">
                  <span className="text-3xl">{platformIcons[opp.platform] || '🔗'}</span>
                  <div>
                    <h3 className="text-lg font-bold text-gray-900">{opp.name}</h3>
                    <span className={`inline-block text-xs font-semibold px-2 py-0.5 rounded border ${platformColors[opp.platform] || 'bg-gray-100 text-gray-700 border-gray-200'}`}>
                      {opp.category}
                    </span>
                  </div>
                </div>
                <div className="text-right">
                  <p className="text-xs text-gray-500">Earn Potential</p>
                  <p className="text-lg font-bold text-green-600">{opp.earnPotential}</p>
                </div>
              </div>

              <p className="text-gray-600 text-sm mb-4">{opp.description}</p>

              <div className="mb-4">
                <p className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-2">Revenue Model</p>
                <p className="text-sm text-gray-700">{opp.revenueModel}</p>
              </div>

              <div className="mb-4">
                <p className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-2">How to Get Started</p>
                <ol className="space-y-1">
                  {opp.steps.map((step, index) => (
                    <li key={index} className="flex items-start text-sm text-gray-600">
                      <span className="text-blue-500 font-semibold mr-2 flex-shrink-0">{index + 1}.</span>
                      {step}
                    </li>
                  ))}
                </ol>
              </div>

              <div className="flex gap-3 mt-4">
                <a
                  href={opp.links.signup}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="bg-blue-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-blue-700 transition-colors"
                >
                  Get Started
                </a>
                <a
                  href={opp.links.docs}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="bg-gray-100 text-gray-700 px-4 py-2 rounded-lg text-sm font-medium hover:bg-gray-200 transition-colors"
                >
                  View Docs
                </a>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default Monetization;
