# Smart Contract Security

Comprehensive guide to securing smart contracts, covering common vulnerabilities, security patterns, and best practices for building resilient Web3 applications.

## 🛡️ Security Fundamentals

### 1. Common Vulnerabilities

#### Reentrancy Attacks
**The Problem:**
```solidity
// ❌ Vulnerable to reentrancy
contract VulnerableContract {
    mapping(address => uint256) public balances;
    
    function withdraw(uint256 amount) external {
        require(balances[msg.sender] >= amount, "Insufficient balance");
        
        // External call before state change - VULNERABLE!
        (bool success, ) = msg.sender.call{value: amount}("");
        require(success, "Transfer failed");
        
        balances[msg.sender] -= amount; // State change after external call
    }
}
```

**The Solution:**
```solidity
// ✅ Protected against reentrancy
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";

contract SecureContract is ReentrancyGuard {
    mapping(address => uint256) public balances;
    
    function withdraw(uint256 amount) external nonReentrant {
        require(balances[msg.sender] >= amount, "Insufficient balance");
        
        // State change before external call
        balances[msg.sender] -= amount;
        
        // External call after state change
        (bool success, ) = msg.sender.call{value: amount}("");
        require(success, "Transfer failed");
    }
}
```

#### Integer Overflow/Underflow
```solidity
// ✅ Safe arithmetic (Solidity 0.8+)
contract SafeArithmetic {
    uint256 public value;
    
    function safeAdd(uint256 amount) external {
        value += amount; // Automatically reverts on overflow in 0.8+
    }
    
    function safeSub(uint256 amount) external {
        value -= amount; // Automatically reverts on underflow in 0.8+
    }
    
    // For older versions, use SafeMath
    using SafeMath for uint256;
    
    function legacySafeAdd(uint256 amount) external {
        value = value.add(amount);
    }
}
```

#### Access Control Vulnerabilities
```solidity
// ✅ Proper access control
import "@openzeppelin/contracts/access/AccessControl.sol";

contract SecureAccessControl is AccessControl {
    bytes32 public constant ADMIN_ROLE = keccak256("ADMIN_ROLE");
    bytes32 public constant OPERATOR_ROLE = keccak256("OPERATOR_ROLE");
    
    constructor() {
        _grantRole(DEFAULT_ADMIN_ROLE, msg.sender);
        _grantRole(ADMIN_ROLE, msg.sender);
    }
    
    function criticalFunction() external onlyRole(ADMIN_ROLE) {
        // Only admins can call this function
    }
    
    function operatorFunction() external onlyRole(OPERATOR_ROLE) {
        // Only operators can call this function
    }
    
    // Multi-signature requirement for critical operations
    mapping(bytes32 => mapping(address => bool)) private _confirmations;
    mapping(bytes32 => uint256) private _confirmationCount;
    uint256 public constant REQUIRED_CONFIRMATIONS = 3;
    
    function proposeTransaction(bytes32 txHash) external onlyRole(ADMIN_ROLE) {
        require(!_confirmations[txHash][msg.sender], "Already confirmed");
        
        _confirmations[txHash][msg.sender] = true;
        _confirmationCount[txHash]++;
        
        if (_confirmationCount[txHash] >= REQUIRED_CONFIRMATIONS) {
            _executeTransaction(txHash);
        }
    }
}
```

### 2. Secure Coding Patterns

#### Check-Effects-Interactions Pattern
```solidity
contract SecureTransfer {
    mapping(address => uint256) public balances;
    
    function transfer(address to, uint256 amount) external {
        // CHECKS: Validate inputs and conditions
        require(to != address(0), "Invalid recipient");
        require(amount > 0, "Amount must be positive");
        require(balances[msg.sender] >= amount, "Insufficient balance");
        
        // EFFECTS: Update state variables
        balances[msg.sender] -= amount;
        balances[to] += amount;
        
        // INTERACTIONS: External calls (if needed)
        emit Transfer(msg.sender, to, amount);
    }
}
```

#### Circuit Breaker Pattern
```solidity
import "@openzeppelin/contracts/security/Pausable.sol";

contract CircuitBreaker is Pausable {
    uint256 public constant MAX_DAILY_WITHDRAWAL = 1000 ether;
    mapping(uint256 => uint256) public dailyWithdrawals; // day => amount
    
    function withdraw(uint256 amount) external whenNotPaused {
        uint256 today = block.timestamp / 86400; // Current day
        
        require(
            dailyWithdrawals[today] + amount <= MAX_DAILY_WITHDRAWAL,
            "Daily withdrawal limit exceeded"
        );
        
        dailyWithdrawals[today] += amount;
        
        // Perform withdrawal
        (bool success, ) = msg.sender.call{value: amount}("");
        require(success, "Transfer failed");
    }
    
    function emergencyPause() external onlyOwner {
        _pause();
    }
    
    function resume() external onlyOwner {
        _unpause();
    }
}
```

#### Rate Limiting
```solidity
contract RateLimited {
    mapping(address => uint256) public lastActionTime;
    uint256 public constant COOLDOWN_PERIOD = 1 hours;
    
    modifier rateLimited() {
        require(
            block.timestamp >= lastActionTime[msg.sender] + COOLDOWN_PERIOD,
            "Action too frequent"
        );
        lastActionTime[msg.sender] = block.timestamp;
        _;
    }
    
    function limitedAction() external rateLimited {
        // Action can only be performed once per hour per address
    }
}
```

## 🔒 Advanced Security Patterns

### 1. Proxy Security
```solidity
// ✅ Secure proxy implementation
import "@openzeppelin/contracts-upgradeable/proxy/utils/Initializable.sol";
import "@openzeppelin/contracts-upgradeable/proxy/utils/UUPSUpgradeable.sol";
import "@openzeppelin/contracts-upgradeable/access/OwnableUpgradeable.sol";

contract SecureUpgradeable is Initializable, UUPSUpgradeable, OwnableUpgradeable {
    uint256 public value;
    
    function initialize(uint256 _value) public initializer {
        __Ownable_init();
        __UUPSUpgradeable_init();
        value = _value;
    }
    
    function _authorizeUpgrade(address newImplementation) 
        internal 
        override 
        onlyOwner 
    {}
    
    // Prevent initialization of implementation contract
    constructor() {
        _disableInitializers();
    }
}
```

### 2. Oracle Security
```solidity
interface IPriceOracle {
    function getPrice(address token) external view returns (uint256, uint256); // price, timestamp
}

contract SecureOracle {
    IPriceOracle[] public oracles;
    uint256 public constant PRICE_TOLERANCE = 500; // 5% tolerance
    uint256 public constant MAX_PRICE_AGE = 300; // 5 minutes
    
    function getSecurePrice(address token) external view returns (uint256) {
        require(oracles.length >= 3, "Insufficient oracles");
        
        uint256[] memory prices = new uint256[](oracles.length);
        uint256 validPrices = 0;
        
        for (uint256 i = 0; i < oracles.length; i++) {
            try oracles[i].getPrice(token) returns (uint256 price, uint256 timestamp) {
                require(block.timestamp - timestamp <= MAX_PRICE_AGE, "Price too old");
                prices[validPrices] = price;
                validPrices++;
            } catch {
                // Skip failed oracle
                continue;
            }
        }
        
        require(validPrices >= 3, "Insufficient valid prices");
        
        // Calculate median price
        uint256 medianPrice = _calculateMedian(prices, validPrices);
        
        // Validate price consistency
        _validatePriceConsistency(prices, validPrices, medianPrice);
        
        return medianPrice;
    }
    
    function _validatePriceConsistency(
        uint256[] memory prices,
        uint256 validCount,
        uint256 median
    ) internal pure {
        for (uint256 i = 0; i < validCount; i++) {
            uint256 deviation = prices[i] > median ? 
                prices[i] - median : median - prices[i];
            uint256 deviationPercent = (deviation * 10000) / median;
            
            require(
                deviationPercent <= PRICE_TOLERANCE,
                "Price deviation too high"
            );
        }
    }
}
```

### 3. Flash Loan Protection
```solidity
contract FlashLoanProtected {
    mapping(address => uint256) private _balanceSnapshots;
    uint256 private _snapshotId;
    
    modifier noFlashLoan() {
        uint256 currentSnapshot = _snapshotId;
        _balanceSnapshots[msg.sender] = address(this).balance;
        _;
        require(
            address(this).balance >= _balanceSnapshots[msg.sender],
            "Flash loan detected"
        );
        require(_snapshotId == currentSnapshot, "Nested calls detected");
        _snapshotId++;
    }
    
    function sensitiveFunction() external noFlashLoan {
        // Protected against flash loan attacks
    }
}
```

## 🔍 Security Testing

### 1. Automated Testing
```javascript
// Comprehensive security test suite
const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("Security Tests", function() {
    let contract, owner, attacker;
    
    beforeEach(async function() {
        [owner, attacker] = await ethers.getSigners();
        const Contract = await ethers.getContractFactory("SecureContract");
        contract = await Contract.deploy();
    });
    
    describe("Reentrancy Protection", function() {
        it("Should prevent reentrancy attacks", async function() {
            // Deploy malicious contract
            const MaliciousContract = await ethers.getContractFactory("ReentrancyAttacker");
            const malicious = await MaliciousContract.deploy(contract.address);
            
            // Attempt reentrancy attack
            await expect(
                malicious.attack({ value: ethers.utils.parseEther("1") })
            ).to.be.revertedWith("ReentrancyGuard: reentrant call");
        });
    });
    
    describe("Access Control", function() {
        it("Should restrict admin functions", async function() {
            await expect(
                contract.connect(attacker).adminFunction()
            ).to.be.revertedWith("AccessControl: account is missing role");
        });
        
        it("Should allow role-based access", async function() {
            await contract.grantRole(OPERATOR_ROLE, attacker.address);
            await expect(
                contract.connect(attacker).operatorFunction()
            ).not.to.be.reverted;
        });
    });
    
    describe("Input Validation", function() {
        it("Should reject invalid inputs", async function() {
            await expect(
                contract.transfer(ethers.constants.AddressZero, 100)
            ).to.be.revertedWith("Invalid recipient");
            
            await expect(
                contract.transfer(attacker.address, 0)
            ).to.be.revertedWith("Amount must be positive");
        });
    });
    
    describe("Economic Attacks", function() {
        it("Should handle large number inputs", async function() {
            const largeNumber = ethers.constants.MaxUint256;
            await expect(
                contract.handleLargeNumber(largeNumber)
            ).not.to.be.reverted;
        });
        
        it("Should prevent overflow/underflow", async function() {
            await expect(
                contract.add(ethers.constants.MaxUint256, 1)
            ).to.be.reverted;
        });
    });
});
```

### 2. Formal Verification
```solidity
// Specify invariants for formal verification
contract VerifiableContract {
    mapping(address => uint256) public balances;
    uint256 public totalSupply;
    
    // Invariant: Total supply equals sum of all balances
    function invariant_totalSupplyConsistency() public view returns (bool) {
        // This would be verified by formal verification tools
        return true; // Placeholder for actual verification logic
    }
    
    // Invariant: No balance can exceed total supply
    function invariant_balanceWithinSupply(address user) public view returns (bool) {
        return balances[user] <= totalSupply;
    }
    
    // Invariant: Total supply never decreases (for non-burnable tokens)
    uint256 public immutable INITIAL_SUPPLY;
    
    constructor(uint256 _initialSupply) {
        INITIAL_SUPPLY = _initialSupply;
        totalSupply = _initialSupply;
    }
    
    function invariant_supplyNeverDecreases() public view returns (bool) {
        return totalSupply >= INITIAL_SUPPLY;
    }
}
```

## 🛠️ Security Tools Integration

### 1. Static Analysis with Slither
```bash
# Install Slither
pip install slither-analyzer

# Run comprehensive analysis
slither contract.sol --detect all

# Custom detector for specific patterns
slither contract.sol --detect reentrancy-eth,controlled-delegatecall
```

### 2. Dynamic Analysis with Echidna
```solidity
// Echidna property testing
contract EchidnaTest {
    SecureContract internal contract_instance;
    
    constructor() {
        contract_instance = new SecureContract();
    }
    
    // Property: Balance should never exceed supply
    function echidna_balance_within_supply() public view returns (bool) {
        return contract_instance.balanceOf(msg.sender) <= 
               contract_instance.totalSupply();
    }
    
    // Property: Transfer should preserve total supply
    function echidna_transfer_preserves_supply() public view returns (bool) {
        return contract_instance.totalSupply() == INITIAL_SUPPLY;
    }
}
```

### 3. Continuous Security Monitoring
```javascript
// Security monitoring service
class SecurityMonitor {
    constructor(contractAddress, web3) {
        this.contract = contractAddress;
        this.web3 = web3;
        this.alerts = [];
    }
    
    async monitorSuspiciousActivity() {
        // Monitor for large transactions
        const subscription = await this.web3.eth.subscribe('pendingTransactions');
        
        subscription.on('data', async (txHash) => {
            const tx = await this.web3.eth.getTransaction(txHash);
            
            if (tx.to === this.contract && tx.value > this.LARGE_TRANSACTION_THRESHOLD) {
                this.generateAlert('Large transaction detected', tx);
            }
        });
    }
    
    async scanForVulnerabilities() {
        // Automated vulnerability scanning
        const contractCode = await this.web3.eth.getCode(this.contract);
        
        // Pattern matching for known vulnerabilities
        const vulnerabilityPatterns = [
            /call\s*\{[^}]*\}\s*\([^)]*\)/, // External calls
            /delegatecall\s*\([^)]*\)/,     // Delegate calls
            /selfdestruct\s*\([^)]*\)/      // Self destruct
        ];
        
        vulnerabilityPatterns.forEach(pattern => {
            if (pattern.test(contractCode)) {
                this.generateAlert('Potential vulnerability pattern detected', pattern);
            }
        });
    }
}
```

## 🤖 AI-Enhanced Security

Leverage the Web3 lippytm ChatGPT.AI platform for:
- **Automated code review** and vulnerability detection
- **Smart contract auditing** assistance
- **Security pattern recognition** and recommendations
- **Real-time threat analysis** and response

## 📊 Security Metrics

Track security posture with:
- **Code coverage** of security tests
- **Vulnerability scan results** and remediation time
- **Incident response times** and effectiveness
- **Security training completion** rates

## 🚨 Incident Response

### Emergency Procedures
1. **Immediate Response**
   - Pause contract operations if possible
   - Assess scope of potential damage
   - Notify stakeholders immediately

2. **Investigation**
   - Analyze transaction logs
   - Identify attack vector
   - Preserve evidence

3. **Recovery**
   - Deploy fixes or upgrades
   - Recover funds if possible
   - Implement additional safeguards

### Emergency Contacts
For critical security incidents: **lippytimemachines@gmail.com**

---

*Security is not a destination but a continuous journey. Stay vigilant, test thoroughly, and never stop learning.*