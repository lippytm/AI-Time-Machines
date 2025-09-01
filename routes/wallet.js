const express = require('express');
const router = express.Router();
const emailService = require('../utils/email');

// Wallet connection notification
router.post('/connect', async (req, res) => {
    try {
        const { walletAddress, timestamp } = req.body;
        
        if (!walletAddress) {
            return res.status(400).json({ 
                success: false, 
                error: 'Wallet address required' 
            });
        }
        
        // Validate wallet address format (basic validation)
        if (!/^0x[a-fA-F0-9]{40}$/.test(walletAddress)) {
            return res.status(400).json({ 
                success: false, 
                error: 'Invalid wallet address format' 
            });
        }
        
        // Log wallet connection
        console.log(`Wallet connected: ${walletAddress} at ${timestamp}`);
        
        // Send email notification about wallet connection
        try {
            await emailService.sendWalletConnectionNotification(walletAddress);
        } catch (emailError) {
            console.error('Failed to send email notification:', emailError);
            // Don't fail the API call if email fails
        }
        
        res.json({
            success: true,
            message: 'Wallet connection recorded',
            walletAddress: walletAddress,
            timestamp: timestamp
        });
        
    } catch (error) {
        console.error('Wallet connect route error:', error);
        res.status(500).json({
            success: false,
            error: 'Internal server error'
        });
    }
});

// Get wallet information
router.get('/info/:address', async (req, res) => {
    try {
        const { address } = req.params;
        
        if (!address || !/^0x[a-fA-F0-9]{40}$/.test(address)) {
            return res.status(400).json({ 
                success: false, 
                error: 'Invalid wallet address' 
            });
        }
        
        // In a real application, you might fetch additional wallet info from blockchain
        res.json({
            success: true,
            walletAddress: address,
            status: 'connected',
            features: {
                payments: true,
                notifications: true,
                aiChat: true
            }
        });
        
    } catch (error) {
        console.error('Wallet info route error:', error);
        res.status(500).json({
            success: false,
            error: 'Failed to get wallet information'
        });
    }
});

// Wallet disconnection
router.post('/disconnect', async (req, res) => {
    try {
        const { walletAddress } = req.body;
        
        console.log(`Wallet disconnected: ${walletAddress}`);
        
        res.json({
            success: true,
            message: 'Wallet disconnection recorded'
        });
        
    } catch (error) {
        console.error('Wallet disconnect route error:', error);
        res.status(500).json({
            success: false,
            error: 'Internal server error'
        });
    }
});

module.exports = router;