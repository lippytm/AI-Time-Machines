// Global variables
let web3Provider = null;
let currentAccount = null;
let isWalletConnected = false;

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 lippytm ChatGPT AI initialized');
    checkWalletConnection();
    setupEventListeners();
});

// Setup event listeners
function setupEventListeners() {
    // Enter key for chat input
    document.getElementById('chatInput').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });

    // Wallet events
    if (window.ethereum) {
        window.ethereum.on('accountsChanged', handleAccountsChanged);
        window.ethereum.on('chainChanged', handleChainChanged);
    }
}

// Wallet Connection Functions
async function connectWallet() {
    try {
        if (typeof window.ethereum === 'undefined') {
            alert('Please install MetaMask or another Web3 wallet!');
            return;
        }

        // Request account access
        const accounts = await window.ethereum.request({
            method: 'eth_requestAccounts'
        });

        if (accounts.length > 0) {
            currentAccount = accounts[0];
            web3Provider = new ethers.providers.Web3Provider(window.ethereum);
            isWalletConnected = true;
            
            updateWalletUI();
            await getAccountInfo();
            
            // Notify backend about wallet connection
            await notifyWalletConnection();
        }
    } catch (error) {
        console.error('Failed to connect wallet:', error);
        alert('Failed to connect wallet: ' + error.message);
    }
}

async function checkWalletConnection() {
    try {
        if (typeof window.ethereum !== 'undefined') {
            const accounts = await window.ethereum.request({
                method: 'eth_accounts'
            });
            
            if (accounts.length > 0) {
                currentAccount = accounts[0];
                web3Provider = new ethers.providers.Web3Provider(window.ethereum);
                isWalletConnected = true;
                updateWalletUI();
                await getAccountInfo();
            }
        }
    } catch (error) {
        console.error('Error checking wallet connection:', error);
    }
}

async function getAccountInfo() {
    try {
        if (!web3Provider || !currentAccount) return;

        const balance = await web3Provider.getBalance(currentAccount);
        const network = await web3Provider.getNetwork();
        
        const balanceInEth = ethers.utils.formatEther(balance);
        
        document.getElementById('walletInfo').innerHTML = `
            <strong>Account:</strong> ${currentAccount.substring(0, 6)}...${currentAccount.substring(38)}<br>
            <strong>Balance:</strong> ${parseFloat(balanceInEth).toFixed(4)} ETH<br>
            <strong>Network:</strong> ${network.name} (${network.chainId})
        `;
    } catch (error) {
        console.error('Error getting account info:', error);
    }
}

function updateWalletUI() {
    const walletStatus = document.getElementById('walletStatus');
    const connectBtn = document.getElementById('connectWalletBtn');
    const paymentBtn = document.getElementById('sendPaymentBtn');
    const paymentStatus = document.getElementById('paymentStatus');

    if (isWalletConnected) {
        walletStatus.className = 'status status-connected';
        walletStatus.textContent = 'Wallet: Connected ✅';
        connectBtn.textContent = 'Disconnect';
        connectBtn.onclick = disconnectWallet;
        
        paymentStatus.className = 'status status-connected';
        paymentStatus.textContent = 'Payment: Ready ✅';
        paymentBtn.disabled = false;
    } else {
        walletStatus.className = 'status status-disconnected';
        walletStatus.textContent = 'Wallet: Disconnected';
        connectBtn.textContent = 'Connect Wallet';
        connectBtn.onclick = connectWallet;
        
        paymentStatus.className = 'status status-disconnected';
        paymentStatus.textContent = 'Payment: Not Ready';
        paymentBtn.disabled = true;
        
        document.getElementById('walletInfo').innerHTML = '';
    }
}

function disconnectWallet() {
    currentAccount = null;
    web3Provider = null;
    isWalletConnected = false;
    updateWalletUI();
}

function handleAccountsChanged(accounts) {
    if (accounts.length === 0) {
        disconnectWallet();
    } else {
        currentAccount = accounts[0];
        getAccountInfo();
    }
}

function handleChainChanged(chainId) {
    // Reload the page to reset state
    window.location.reload();
}

// Chat Functions
async function sendMessage() {
    const input = document.getElementById('chatInput');
    const message = input.value.trim();
    
    if (!message) return;
    
    // Add user message to chat
    addMessageToChat('user', message);
    input.value = '';
    
    // Show loading
    showLoading(true);
    
    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message: message,
                walletConnected: isWalletConnected,
                walletAddress: currentAccount
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            addMessageToChat('ai', data.response);
        } else {
            addMessageToChat('ai', 'Sorry, I encountered an error. Please try again.');
        }
    } catch (error) {
        console.error('Chat error:', error);
        addMessageToChat('ai', 'Connection error. Please check your internet connection.');
    } finally {
        showLoading(false);
    }
}

function addMessageToChat(sender, message) {
    const chatContainer = document.getElementById('chatContainer');
    const messageDiv = document.createElement('div');
    
    if (sender === 'user') {
        messageDiv.className = 'message user-message';
        messageDiv.innerHTML = `<strong>You:</strong> ${escapeHtml(message)}`;
    } else {
        messageDiv.className = 'message ai-message';
        messageDiv.innerHTML = `<strong>AI Assistant:</strong> ${escapeHtml(message)}`;
    }
    
    chatContainer.appendChild(messageDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

function showLoading(show) {
    const loading = document.getElementById('chatLoading');
    loading.style.display = show ? 'block' : 'none';
}

// Payment Functions
async function sendPayment() {
    if (!isWalletConnected || !web3Provider) {
        alert('Please connect your wallet first!');
        return;
    }

    const amount = document.getElementById('paymentAmount').value;
    if (!amount || parseFloat(amount) <= 0) {
        alert('Please enter a valid amount!');
        return;
    }

    try {
        const signer = web3Provider.getSigner();
        
        // Convert amount to Wei
        const amountWei = ethers.utils.parseEther(amount);
        
        // Send transaction (you can replace this with your own payment logic)
        const tx = await signer.sendTransaction({
            to: '0x0000000000000000000000000000000000000000', // Replace with your payment address
            value: amountWei
        });
        
        alert(`Payment sent! Transaction hash: ${tx.hash}`);
        
        // Notify backend about payment
        await notifyPayment(tx.hash, amount);
        
    } catch (error) {
        console.error('Payment error:', error);
        alert('Payment failed: ' + error.message);
    }
}

// Notification Functions
async function testNotification() {
    try {
        const response = await fetch('/api/payment/test-notification', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                walletAddress: currentAccount
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            alert('Test notification sent successfully!');
        } else {
            alert('Failed to send notification: ' + data.error);
        }
    } catch (error) {
        console.error('Notification error:', error);
        alert('Failed to send notification');
    }
}

// Backend Communication Functions
async function notifyWalletConnection() {
    try {
        await fetch('/api/wallet/connect', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                walletAddress: currentAccount,
                timestamp: new Date().toISOString()
            })
        });
    } catch (error) {
        console.error('Failed to notify wallet connection:', error);
    }
}

async function notifyPayment(txHash, amount) {
    try {
        await fetch('/api/payment/notify', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                walletAddress: currentAccount,
                transactionHash: txHash,
                amount: amount,
                timestamp: new Date().toISOString()
            })
        });
    } catch (error) {
        console.error('Failed to notify payment:', error);
    }
}

// Utility Functions
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Error Handling
window.addEventListener('error', function(e) {
    console.error('Global error:', e.error);
});

// Wallet detection
if (typeof window.ethereum === 'undefined') {
    console.warn('No Web3 wallet detected. Please install MetaMask or another Web3 wallet.');
}