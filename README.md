# AI-Time-Machines
## lippytm ChatGPT AI with Web3 Wallet & Payment Integration

A Web3-enabled ChatGPT AI assistant with integrated wallet connectivity and payment system. This application allows users to interact with an AI assistant while performing decentralized transactions seamlessly.

### 🚀 Features

- **AI Chat Interface**: Interactive ChatGPT-powered AI assistant
- **Web3 Wallet Integration**: MetaMask and other Web3 wallet support
- **Decentralized Payments**: ETH transaction capabilities
- **Email Notifications**: Automated notifications to lippytimemachines@gmail.com
- **Security-First Design**: Rate limiting, input validation, and secure practices
- **Responsive UI**: Modern, mobile-friendly interface

### 🛠️ Technology Stack

- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Backend**: Node.js, Express.js
- **Web3**: ethers.js for blockchain interactions
- **Email**: Nodemailer for email notifications
- **Security**: Helmet, CORS, rate limiting

### 📋 Prerequisites

- Node.js 16.0.0 or higher
- npm or yarn package manager
- Web3 wallet (MetaMask recommended)
- Gmail account with app password (for notifications)

### 🔧 Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/lippytm/AI-Time-Machines.git
   cd AI-Time-Machines
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Environment Configuration**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` file with your configuration:
   ```env
   # OpenAI API Configuration (optional - demo mode available)
   OPENAI_API_KEY=your_openai_api_key_here

   # Email Configuration
   EMAIL_SERVICE=gmail
   EMAIL_USER=lippytimemachines@gmail.com
   EMAIL_PASS=your_gmail_app_password_here

   # Server Configuration
   PORT=3000
   NODE_ENV=development

   # Security
   JWT_SECRET=your_jwt_secret_here
   RATE_LIMIT_WINDOW_MS=900000
   RATE_LIMIT_MAX_REQUESTS=100
   ```

4. **Gmail App Password Setup**
   - Enable 2-factor authentication on your Gmail account
   - Generate an app password: Google Account > Security > App passwords
   - Use the generated password in `EMAIL_PASS`

5. **Start the application**
   ```bash
   npm start
   ```

6. **Access the application**
   Open http://localhost:3000 in your browser

### 🔐 Web3 Wallet Setup

1. **Install MetaMask**: Download from [metamask.io](https://metamask.io/)
2. **Create/Import Wallet**: Set up your Ethereum wallet
3. **Connect to App**: Click "Connect Wallet" in the application
4. **Test Payment**: Use small amounts on testnets first

### 💰 Payment System

The payment system supports:
- **ETH Transactions**: Direct Ethereum payments
- **Transaction Notifications**: Email alerts for all payments
- **Security Validation**: Address and transaction hash verification
- **Error Handling**: Comprehensive error messages

### 📧 Email Notification System

Automated notifications are sent to `lippytimemachines@gmail.com` for:
- New wallet connections
- Payment transactions
- System alerts
- Test notifications

### 🔒 Security Features

- **Rate Limiting**: Prevents API abuse
- **Input Validation**: Sanitizes all user inputs
- **CORS Protection**: Configured for production security
- **Helmet.js**: Security headers and CSP
- **Address Validation**: Ethereum address format verification
- **Transaction Verification**: Hash format validation

### 🧪 Testing

1. **Connect Wallet**: Use MetaMask on a testnet
2. **Test Chat**: Send messages to the AI assistant
3. **Test Payments**: Send small testnet transactions
4. **Test Notifications**: Use the "Test Notification" button

### 📱 API Endpoints

#### Chat API
- `POST /api/chat` - Send message to AI assistant
- `GET /api/chat/history` - Get chat history (future feature)

#### Wallet API
- `POST /api/wallet/connect` - Notify wallet connection
- `GET /api/wallet/info/:address` - Get wallet information
- `POST /api/wallet/disconnect` - Notify wallet disconnection

#### Payment API
- `POST /api/payment/notify` - Payment notification
- `GET /api/payment/history/:address` - Payment history (future feature)
- `POST /api/payment/test-notification` - Send test notification

### 🚀 Deployment

1. **Production Environment**
   ```bash
   NODE_ENV=production npm start
   ```

2. **Environment Variables**
   - Set all required environment variables
   - Use production-grade email service
   - Configure proper CORS origins

3. **Security Checklist**
   - [ ] SSL/TLS certificate installed
   - [ ] Environment variables secured
   - [ ] Rate limiting configured
   - [ ] Email service configured
   - [ ] Wallet addresses validated

### 🔧 Development

```bash
# Install development dependencies
npm install

# Start development server
npm run dev

# Check application health
curl http://localhost:3000/health
```

### 📝 Future Enhancements

- [ ] OpenAI GPT-4 integration
- [ ] Multi-chain support (Polygon, BSC)
- [ ] Payment history dashboard
- [ ] User authentication system
- [ ] Smart contract integration
- [ ] Advanced AI features

### 🐛 Troubleshooting

**Wallet Connection Issues:**
- Ensure MetaMask is installed and unlocked
- Check network connectivity
- Try refreshing the page

**Email Notifications Not Working:**
- Verify Gmail app password
- Check environment variables
- Ensure 2FA is enabled on Gmail account

**Payment Failures:**
- Check wallet balance
- Verify network fees
- Ensure correct network selection

### 📄 License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

### 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

### 📞 Support

For support and questions:
- Email: lippytimemachines@gmail.com
- GitHub Issues: [Create an issue](https://github.com/lippytm/AI-Time-Machines/issues)

---

**© 2024 lippytm AI Time Machines | Web3 & AI Integration**
