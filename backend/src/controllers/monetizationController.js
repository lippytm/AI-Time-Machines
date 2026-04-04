// Monetization controller - subscription plans, revenue opportunities, and partner integrations

// Get available subscription plans
const getPlans = async (req, res) => {
  try {
    const plans = [
      {
        id: 'free',
        name: 'Free',
        price: 0,
        currency: 'USD',
        interval: 'month',
        description: 'Get started with AI Time Machines at no cost',
        features: [
          '3 time series datasets',
          '2 AI models',
          '10 predictions per month',
          'CSV & JSON export',
          'Community support'
        ],
        limits: {
          timeSeries: 3,
          models: 2,
          predictionsPerMonth: 10,
          integrations: 1
        },
        highlighted: false
      },
      {
        id: 'pro',
        name: 'Pro',
        price: 29,
        currency: 'USD',
        interval: 'month',
        description: 'For individuals and small teams monetizing AI predictions',
        features: [
          'Unlimited time series datasets',
          '20 AI models',
          '500 predictions per month',
          'All export formats (CSV, JSON, XML)',
          'ChatGPT integration',
          'Grok (xAI) integration',
          'ManyChat & BotBuilders automation',
          'Replit deployment',
          'Priority support',
          'Revenue analytics'
        ],
        limits: {
          timeSeries: -1,
          models: 20,
          predictionsPerMonth: 500,
          integrations: 5
        },
        highlighted: true
      },
      {
        id: 'enterprise',
        name: 'Enterprise',
        price: 99,
        currency: 'USD',
        interval: 'month',
        description: 'For businesses scaling AI-powered revenue across all platforms',
        features: [
          'Unlimited everything',
          'All Pro features',
          'White-label exports',
          'Custom AI model training',
          'Dedicated ChatGPT & Grok quotas',
          'BotBuilders enterprise bots',
          'ManyChat enterprise flows',
          'Replit Teams deployment',
          'SLA & dedicated support',
          'Custom integrations',
          'Revenue sharing program'
        ],
        limits: {
          timeSeries: -1,
          models: -1,
          predictionsPerMonth: -1,
          integrations: -1
        },
        highlighted: false
      }
    ];

    res.json({ plans });
  } catch (error) {
    console.error('Get plans error:', error);
    res.status(500).json({ error: { message: 'Failed to fetch plans' } });
  }
};

// Get monetization opportunities and partner information
const getOpportunities = async (req, res) => {
  try {
    const opportunities = [
      {
        platform: 'chatgpt',
        name: 'ChatGPT / OpenAI',
        category: 'AI Assistant',
        revenueModel: 'API reselling & consulting',
        description: 'Build and sell ChatGPT-powered prediction bots. Export AI Time Machines forecasts directly into OpenAI assistants to create premium chatbot services.',
        earnPotential: '$500–$5,000/month',
        steps: [
          'Connect your OpenAI API key in Integrations',
          'Export predictions in ChatGPT format',
          'Build custom GPT assistants powered by your forecasts',
          'Offer forecast-powered chatbots as a service'
        ],
        links: {
          signup: 'https://platform.openai.com/signup',
          docs: 'https://platform.openai.com/docs'
        }
      },
      {
        platform: 'grok',
        name: 'Grok (xAI)',
        category: 'AI Assistant',
        revenueModel: 'Real-time analysis & premium reports',
        description: 'Use xAI Grok to deliver real-time market analysis powered by your AI Time Machines predictions. Sell premium analysis reports to subscribers.',
        earnPotential: '$300–$3,000/month',
        steps: [
          'Connect your xAI API key in Integrations',
          'Export predictions in Grok format',
          'Generate real-time analysis reports',
          'Sell premium reports via subscription'
        ],
        links: {
          signup: 'https://x.ai',
          docs: 'https://docs.x.ai'
        }
      },
      {
        platform: 'replit',
        name: 'Replit',
        category: 'Cloud Development',
        revenueModel: 'App deployment & SaaS products',
        description: 'Deploy AI Time Machines prediction tools as standalone apps on Replit. Sell or license your AI apps to other developers and businesses.',
        earnPotential: '$200–$2,000/month',
        steps: [
          'Export predictions in Replit format',
          'Deploy your AI app on Replit with one click',
          'Publish to Replit marketplace',
          'Earn from subscriptions and app sales'
        ],
        links: {
          signup: 'https://replit.com/signup',
          docs: 'https://docs.replit.com'
        }
      },
      {
        platform: 'manychat',
        name: 'ManyChat',
        category: 'Chatbot Marketing',
        revenueModel: 'Lead generation & e-commerce automation',
        description: 'Power ManyChat chatbots with AI Time Machines predictions for sales forecasting, inventory management, and automated customer marketing.',
        earnPotential: '$1,000–$10,000/month',
        steps: [
          'Connect your ManyChat account in Integrations',
          'Export predictions in ManyChat format',
          'Set up automated chat flows with prediction data',
          'Offer prediction-powered chatbot automation services'
        ],
        links: {
          signup: 'https://manychat.com',
          docs: 'https://manychat.com/blog/chatbot-tutorial'
        }
      },
      {
        platform: 'botbuilders',
        name: 'BotBuilders',
        category: 'Chatbot Builder',
        revenueModel: 'Multi-platform bot services',
        description: 'Build SMS, WhatsApp, and Telegram bots driven by AI Time Machines forecasts. Offer automated prediction delivery as a subscription service.',
        earnPotential: '$500–$5,000/month',
        steps: [
          'Connect your BotBuilders account in Integrations',
          'Export predictions in BotBuilders format',
          'Build multi-channel prediction bots',
          'Charge subscribers for automated forecast delivery'
        ],
        links: {
          signup: 'https://botbuilders.com',
          docs: 'https://botbuilders.com/docs'
        }
      }
    ];

    res.json({ opportunities });
  } catch (error) {
    console.error('Get opportunities error:', error);
    res.status(500).json({ error: { message: 'Failed to fetch opportunities' } });
  }
};

// Get revenue summary for user (placeholder for future billing integration)
const getRevenueSummary = async (req, res) => {
  try {
    // Placeholder data – replace with real billing/analytics data when payment processor is integrated
    const summary = {
      currentPlan: 'free',
      activeIntegrations: 0,
      totalPredictionsSent: 0,
      estimatedMonthlyRevenue: 0,
      currency: 'USD',
      message: 'Upgrade to Pro or Enterprise to start generating revenue from your AI predictions.'
    };

    res.json({ summary });
  } catch (error) {
    console.error('Get revenue summary error:', error);
    res.status(500).json({ error: { message: 'Failed to fetch revenue summary' } });
  }
};

module.exports = {
  getPlans,
  getOpportunities,
  getRevenueSummary
};
