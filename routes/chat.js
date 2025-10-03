const express = require('express');
const router = express.Router();

// Mock OpenAI API for demonstration (replace with actual OpenAI API)
// Note: You would normally use the official openai package here
async function getChatGPTResponse(message, context = {}) {
    // This is a mock response. In production, you would use:
    // const { Configuration, OpenAIApi } = require("openai");
    
    try {
        // Mock responses based on message content for demonstration
        if (message.toLowerCase().includes('web3') || message.toLowerCase().includes('wallet')) {
            return "I can help you with Web3 and wallet-related questions! Your wallet connection status allows me to provide personalized blockchain assistance.";
        }
        
        if (message.toLowerCase().includes('payment') || message.toLowerCase().includes('transaction')) {
            return "I can assist with payment and transaction queries. Make sure your wallet is connected for secure transaction processing.";
        }
        
        if (message.toLowerCase().includes('hello') || message.toLowerCase().includes('hi')) {
            return `Hello! I'm your Web3-enabled AI assistant. ${context.walletConnected ? 'I see your wallet is connected - great!' : 'Consider connecting your wallet for enhanced features.'} How can I help you today?`;
        }
        
        // Default response
        return `I understand you're asking about: "${message}". As a Web3-enabled AI assistant, I can help with blockchain, cryptocurrency, smart contracts, and general AI assistance. ${context.walletConnected ? 'Your wallet connection enables secure transaction features.' : 'Connect your wallet for additional Web3 capabilities.'}`;
        
    } catch (error) {
        console.error('Chat API error:', error);
        throw new Error('Failed to get AI response');
    }
}

// Chat endpoint
router.post('/', async (req, res) => {
    try {
        const { message, walletConnected, walletAddress } = req.body;
        
        if (!message || typeof message !== 'string') {
            return res.status(400).json({ 
                success: false, 
                error: 'Invalid message' 
            });
        }
        
        // Sanitize input
        const sanitizedMessage = message.trim().substring(0, 500);
        
        // Prepare context for AI
        const context = {
            walletConnected: walletConnected || false,
            walletAddress: walletAddress || null,
            timestamp: new Date().toISOString()
        };
        
        // Get AI response
        const aiResponse = await getChatGPTResponse(sanitizedMessage, context);
        
        // Log the interaction (in production, you might want to store this in a database)
        console.log(`Chat interaction: ${walletAddress || 'anonymous'} - ${sanitizedMessage}`);
        
        res.json({
            success: true,
            response: aiResponse,
            context: context
        });
        
    } catch (error) {
        console.error('Chat route error:', error);
        res.status(500).json({
            success: false,
            error: 'Internal server error'
        });
    }
});

// Chat history endpoint (for future enhancement)
router.get('/history', async (req, res) => {
    try {
        // This would typically fetch from a database
        res.json({
            success: true,
            history: [],
            message: 'Chat history feature not implemented yet'
        });
    } catch (error) {
        console.error('Chat history error:', error);
        res.status(500).json({
            success: false,
            error: 'Failed to fetch chat history'
        });
    }
});

module.exports = router;