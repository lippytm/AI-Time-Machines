const express = require('express');
const router = express.Router();
const emailService = require('../utils/email');

// Payment notification endpoint
router.post('/notify', async (req, res) => {
    try {
        const { walletAddress, transactionHash, amount, timestamp } = req.body;
        
        // Validate required fields
        if (!walletAddress || !transactionHash || !amount) {
            return res.status(400).json({ 
                success: false, 
                error: 'Missing required payment information' 
            });
        }
        
        // Validate wallet address
        if (!/^0x[a-fA-F0-9]{40}$/.test(walletAddress)) {
            return res.status(400).json({ 
                success: false, 
                error: 'Invalid wallet address format' 
            });
        }
        
        // Validate transaction hash
        if (!/^0x[a-fA-F0-9]{64}$/.test(transactionHash)) {
            return res.status(400).json({ 
                success: false, 
                error: 'Invalid transaction hash format' 
            });
        }
        
        // Validate amount
        const amountNum = parseFloat(amount);
        if (isNaN(amountNum) || amountNum <= 0) {
            return res.status(400).json({ 
                success: false, 
                error: 'Invalid amount' 
            });
        }
        
        // Log payment
        console.log(`Payment received: ${amountNum} ETH from ${walletAddress} - TX: ${transactionHash}`);
        
        // Send email notification about payment
        try {
            await emailService.sendPaymentNotification({
                walletAddress,
                transactionHash,
                amount: amountNum,
                timestamp: timestamp || new Date().toISOString()
            });
        } catch (emailError) {
            console.error('Failed to send payment email notification:', emailError);
        }
        
        res.json({
            success: true,
            message: 'Payment notification recorded',
            paymentInfo: {
                walletAddress,
                transactionHash,
                amount: amountNum,
                timestamp: timestamp || new Date().toISOString()
            }
        });
        
    } catch (error) {
        console.error('Payment notify route error:', error);
        res.status(500).json({
            success: false,
            error: 'Internal server error'
        });
    }
});

// Get payment history (placeholder for future enhancement)
router.get('/history/:address', async (req, res) => {
    try {
        const { address } = req.params;
        
        if (!address || !/^0x[a-fA-F0-9]{40}$/.test(address)) {
            return res.status(400).json({ 
                success: false, 
                error: 'Invalid wallet address' 
            });
        }
        
        // In a real application, you would fetch from a database
        res.json({
            success: true,
            walletAddress: address,
            payments: [],
            message: 'Payment history feature not implemented yet'
        });
        
    } catch (error) {
        console.error('Payment history route error:', error);
        res.status(500).json({
            success: false,
            error: 'Failed to get payment history'
        });
    }
});

// Test notification endpoint
router.post('/test-notification', async (req, res) => {
    try {
        const { walletAddress } = req.body;
        
        // Send test email notification
        try {
            await emailService.sendTestNotification(walletAddress);
            
            res.json({
                success: true,
                message: 'Test notification sent successfully'
            });
        } catch (emailError) {
            console.error('Test notification failed:', emailError);
            res.status(500).json({
                success: false,
                error: 'Failed to send test notification'
            });
        }
        
    } catch (error) {
        console.error('Test notification route error:', error);
        res.status(500).json({
            success: false,
            error: 'Internal server error'
        });
    }
});

module.exports = router;