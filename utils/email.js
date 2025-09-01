const nodemailer = require('nodemailer');

class EmailService {
    constructor() {
        this.transporter = null;
        this.initializeTransporter();
    }

    initializeTransporter() {
        try {
            this.transporter = nodemailer.createTransport({
                service: process.env.EMAIL_SERVICE || 'gmail',
                auth: {
                    user: process.env.EMAIL_USER || 'lippytimemachines@gmail.com',
                    pass: process.env.EMAIL_PASS || '' // App password for Gmail
                }
            });

            // Verify connection
            this.transporter.verify((error, success) => {
                if (error) {
                    console.error('Email service configuration error:', error);
                } else {
                    console.log('📧 Email service ready');
                }
            });
        } catch (error) {
            console.error('Failed to initialize email service:', error);
        }
    }

    async sendWalletConnectionNotification(walletAddress) {
        try {
            if (!this.transporter) {
                throw new Error('Email service not configured');
            }

            const mailOptions = {
                from: process.env.EMAIL_USER || 'lippytimemachines@gmail.com',
                to: 'lippytimemachines@gmail.com',
                subject: '🔐 New Wallet Connection - lippytm ChatGPT AI',
                html: `
                    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                        <h2 style="color: #667eea;">🔐 New Wallet Connection</h2>
                        <p>A new wallet has been connected to the lippytm ChatGPT AI system.</p>
                        
                        <div style="background: #f5f5f5; padding: 15px; border-radius: 8px; margin: 20px 0;">
                            <strong>Wallet Address:</strong> ${walletAddress}<br>
                            <strong>Timestamp:</strong> ${new Date().toISOString()}<br>
                            <strong>Service:</strong> lippytm ChatGPT AI Web3
                        </div>
                        
                        <p>This wallet can now:</p>
                        <ul>
                            <li>✅ Access AI chat services</li>
                            <li>✅ Make decentralized payments</li>
                            <li>✅ Receive transaction notifications</li>
                        </ul>
                        
                        <hr style="margin: 30px 0;">
                        <p style="color: #666; font-size: 12px;">
                            This is an automated notification from lippytm AI Time Machines.<br>
                            Web3 & AI Integration System
                        </p>
                    </div>
                `
            };

            const result = await this.transporter.sendMail(mailOptions);
            console.log('Wallet connection email sent:', result.messageId);
            return result;
        } catch (error) {
            console.error('Failed to send wallet connection email:', error);
            throw error;
        }
    }

    async sendPaymentNotification(paymentInfo) {
        try {
            if (!this.transporter) {
                throw new Error('Email service not configured');
            }

            const { walletAddress, transactionHash, amount, timestamp } = paymentInfo;

            const mailOptions = {
                from: process.env.EMAIL_USER || 'lippytimemachines@gmail.com',
                to: 'lippytimemachines@gmail.com',
                subject: '💰 Payment Received - lippytm ChatGPT AI',
                html: `
                    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                        <h2 style="color: #48bb78;">💰 Payment Received</h2>
                        <p>A payment has been processed through the lippytm ChatGPT AI Web3 system.</p>
                        
                        <div style="background: #f0fff4; padding: 15px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #48bb78;">
                            <strong>Amount:</strong> ${amount} ETH<br>
                            <strong>From:</strong> ${walletAddress}<br>
                            <strong>Transaction Hash:</strong> 
                            <a href="https://etherscan.io/tx/${transactionHash}" target="_blank" style="color: #667eea; word-break: break-all;">
                                ${transactionHash}
                            </a><br>
                            <strong>Timestamp:</strong> ${timestamp}
                        </div>
                        
                        <p style="color: #2d3748;">
                            <strong>Status:</strong> <span style="color: #48bb78;">✅ Confirmed</span>
                        </p>
                        
                        <hr style="margin: 30px 0;">
                        <p style="color: #666; font-size: 12px;">
                            This is an automated notification from lippytm AI Time Machines.<br>
                            Web3 & AI Integration System | 
                            <a href="https://etherscan.io/tx/${transactionHash}" target="_blank">View on Etherscan</a>
                        </p>
                    </div>
                `
            };

            const result = await this.transporter.sendMail(mailOptions);
            console.log('Payment notification email sent:', result.messageId);
            return result;
        } catch (error) {
            console.error('Failed to send payment notification email:', error);
            throw error;
        }
    }

    async sendTestNotification(walletAddress = null) {
        try {
            if (!this.transporter) {
                throw new Error('Email service not configured');
            }

            const mailOptions = {
                from: process.env.EMAIL_USER || 'lippytimemachines@gmail.com',
                to: 'lippytimemachines@gmail.com',
                subject: '🧪 Test Notification - lippytm ChatGPT AI',
                html: `
                    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                        <h2 style="color: #ed8936;">🧪 Test Notification</h2>
                        <p>This is a test notification from the lippytm ChatGPT AI Web3 system.</p>
                        
                        <div style="background: #fffaf0; padding: 15px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #ed8936;">
                            <strong>Test Type:</strong> Email Service Verification<br>
                            <strong>Triggered by:</strong> ${walletAddress || 'System'}<br>
                            <strong>Timestamp:</strong> ${new Date().toISOString()}<br>
                            <strong>Status:</strong> ✅ Email service operational
                        </div>
                        
                        <p>All notification systems are functioning correctly:</p>
                        <ul>
                            <li>✅ SMTP Connection</li>
                            <li>✅ Email Formatting</li>
                            <li>✅ Delivery System</li>
                        </ul>
                        
                        <hr style="margin: 30px 0;">
                        <p style="color: #666; font-size: 12px;">
                            This is an automated test notification from lippytm AI Time Machines.<br>
                            Web3 & AI Integration System
                        </p>
                    </div>
                `
            };

            const result = await this.transporter.sendMail(mailOptions);
            console.log('Test notification email sent:', result.messageId);
            return result;
        } catch (error) {
            console.error('Failed to send test notification email:', error);
            throw error;
        }
    }

    async sendSystemAlert(alertType, message, data = {}) {
        try {
            if (!this.transporter) {
                throw new Error('Email service not configured');
            }

            const mailOptions = {
                from: process.env.EMAIL_USER || 'lippytimemachines@gmail.com',
                to: 'lippytimemachines@gmail.com',
                subject: `🚨 System Alert: ${alertType} - lippytm ChatGPT AI`,
                html: `
                    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                        <h2 style="color: #e53e3e;">🚨 System Alert</h2>
                        <p><strong>Alert Type:</strong> ${alertType}</p>
                        <p><strong>Message:</strong> ${message}</p>
                        
                        ${Object.keys(data).length > 0 ? `
                        <div style="background: #fed7d7; padding: 15px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #e53e3e;">
                            <strong>Additional Data:</strong><br>
                            ${Object.entries(data).map(([key, value]) => `<strong>${key}:</strong> ${value}<br>`).join('')}
                        </div>
                        ` : ''}
                        
                        <p><strong>Timestamp:</strong> ${new Date().toISOString()}</p>
                        
                        <hr style="margin: 30px 0;">
                        <p style="color: #666; font-size: 12px;">
                            This is an automated alert from lippytm AI Time Machines.<br>
                            Web3 & AI Integration System
                        </p>
                    </div>
                `
            };

            const result = await this.transporter.sendMail(mailOptions);
            console.log('System alert email sent:', result.messageId);
            return result;
        } catch (error) {
            console.error('Failed to send system alert email:', error);
            throw error;
        }
    }
}

module.exports = new EmailService();