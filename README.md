# ROA CORE Token Analysis Tools

A collection of Python scripts for querying and analyzing top holders of the ROA CORE token.

## 🎯 Overview

This project provides tools for querying and analyzing top holder information for the ROA CORE token (`5tB5D6DGJMxxHYmNkfJNG237x6pZGEwTzGpUUh62yQJ7`) on the Solana blockchain.

## 📁 File Structure

```
├── network_test.py                 # RPC connection test
├── tokenstats.py                   # Token Top Holders
└── README.md                       # Project Description
```

## 🔧 Requirements

### Python Version

- Python 3.11+ recommended

### Required Packages

```bash
pip install requests
```

## 🚀 Installation & Usage

### 1. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python -m venv venv
source venv/bin/activate
```

### 2. Install Packages

```bash
pip install requests
```

### 3. Run Scripts

```bash
# RPC Connection Test
python network_test.py

# Basic Token Analysis
python tokenstats.py

# Advanced Diagnostics Analysis
# python token_stats_enhanced.py
```

## 📊 Script Descriptions

### 1. Network Test (`network_test.py`)

**Purpose:** Check basic connection status of Solana RPC endpoints

**Features:**

- RPC endpoint connection testing
- Basic status check through `getHealth` API calls
- Response time and error handling

**Use Case:** When you need to verify if RPC service is working properly

### 2. Basic Token Analysis (`tokenstats.py`)

**Purpose:** Query top holder information for ROA CORE token

**Features:**

- Query total token supply
- List of top large account holders
- Calculate balance and percentage per holder
- JSON format output

**Sample Output:**

```
🏆 Top Holders List
============================================================
1. Address: ABC123...XYZ789
   Balance: 1,234,567.890000 ROA
------------------------------------------------------------
📊 Top 5 Holders Total Balance: 12,345,678.90 ROA
🎯 Percentage of Total Supply: 15.67%
```

### 3. Advanced Diagnostics Analysis (`token_stats_enhanced.py`)

**Purpose:** Comprehensive RPC performance analysis and token data querying

**Advanced Features:**

- **RPC Function Testing**: Check supported methods for each endpoint
- **Response Time Measurement**: Accurate performance analysis
- **Multiple Method Attempts**: Retry with various parameter combinations
- **Automatic Endpoint Selection**: Auto-select most stable RPC
- **Detailed Performance Report**: Total duration, data size, etc.

**Performance Analysis Example:**

```
🔍 RPC Function Test: https://api.mainnet-beta.solana.com
   Test: Basic Connection (getHealth)
   Response Time: 0.45s
   ✅ Success (Data Size: 156 bytes)

📈 Performance Info:
   - Token Supply Query: 1.23s
   - Large Account Query: 2.45s
   - Total Duration: 3.68s
```

## 🌐 Supported RPC Endpoints

### Public RPCs

- **Solana Official:** `https://api.mainnet-beta.solana.com`
- **Ankr:** `https://rpc.ankr.com/solana`

### Premium RPCs

- **QuickNode:** Personal URL required
- **Alchemy:** Personal API key required
- **Helius:** Personal API key required

## ⚠️ Important Notes

### RPC Limitations

1. **Public RPC Limitations:**

   - Rate limiting (requests per minute limit)
   - Some advanced methods not supported
   - Slow response times (5-30 seconds)
   - Occasional service interruptions

2. **Premium RPC Benefits:**
   - Higher request limits
   - All RPC methods supported
   - Fast response times (1-3 seconds)
   - Stable service

### Performance Optimization Recommendations

1. **Use Premium RPC**

   ```python
   # QuickNode example
   endpoints = [
       "https://your-quicknode-endpoint.quiknode.pro/your-api-key/"
   ]
   ```

2. **Set Appropriate Timeouts**

   ```python
   response = requests.post(endpoint, json=payload, timeout=60)
   ```

3. **Add Delays Between Requests**
   ```python
   time.sleep(2)  # Wait 2 seconds
   ```

## 🔍 Troubleshooting

### Common Errors

1. **`AttributeError: 'dict' object has no attribute 'offset'`**

   - **Cause:** solana library version compatibility issue
   - **Solution:** Use `tokenstats.py` (pure requests method)

2. **`Timeout Error`**

   - **Cause:** RPC response delay
   - **Solution:** Increase timeout value or use premium RPC

3. **`RPC Error: Method not found`**

   - **Cause:** The RPC doesn't support specific methods
   - **Solution:** Try different RPC endpoints

4. **`Rate limiting`**
   - **Cause:** Request limit exceeded
   - **Solution:** Add delay between requests

## 📈 Using Analysis Results

### JSON Data Structure

```json
[
  {
    "address": "holder_address",
    "balance": 1234567.89
  },
  ...
]
```

### Data Usage Examples

```python
# Calculate top holder percentage
top5_balance = sum(holder['balance'] for holder in holders[:5])
percentage = (top5_balance / total_supply) * 100

# Filter holders with specific balance threshold
large_holders = [h for h in holders if h['balance'] > 100000]
```

## 🔗 Useful Links

### Blockchain Explorers

- **Solscan:** https://solscan.io/token/5tB5D6DGJMxxHYmNkfJNG237x6pZGEwTzGpUUh62yQJ7
- **Solana Explorer:** https://explorer.solana.com/address/5tB5D6DGJMxxHYmNkfJNG237x6pZGEwTzGpUUh62yQJ7
- **SolanaFM:** https://solana.fm/address/5tB5D6DGJMxxHYmNkfJNG237x6pZGEwTzGpUUh62yQJ7

### RPC Services

- **QuickNode:** https://www.quicknode.com/
- **Alchemy:** https://www.alchemy.com/
- **Helius:** https://helius.xyz/

## 🤝 Contributing

If you'd like to contribute to this project:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is distributed under the MIT License.

## ⚡ Quick Start

```bash
# 1. Clone and setup
git clone <repository-url>
cd roa-token-analysis
python -m venv venv
venv\Scripts\activate  # Windows
pip install requests

# 2. Run basic analysis
python tokenstats.py

# 3. Run advanced analysis
python token_stats_enhanced.py
```

---

**Last Updated:** 2025-12-18
