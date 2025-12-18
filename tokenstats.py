# token_stats_enhanced_en.py
import requests
import json
import time
from datetime import datetime

ROACORE_TOKEN_MINT = "5tB5D6DGJMxxHYmNkfJNG237x6pZGEwTzGpUUh62yQJ7"


def call_solana_rpc_with_timing(endpoint, method, params=None, timeout=60):
    """Call Solana RPC with response time measurement"""

    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": method
    }

    if params:
        payload["params"] = params

    start_time = time.time()

    try:
        response = requests.post(endpoint, json=payload, timeout=timeout)
        end_time = time.time()
        response_time = end_time - start_time

        print(f"   Response time: {response_time:.2f}s")

        if response.status_code == 200:
            result = response.json()
            if 'error' in result:
                error_details = result['error']
                raise Exception(f"RPC Error: {error_details}")
            return result['result'], response_time
        else:
            raise Exception(f"HTTP Error: {response.status_code}")

    except requests.exceptions.Timeout:
        end_time = time.time()
        response_time = end_time - start_time
        raise Exception(f"Timeout after {response_time:.2f} seconds")
    except requests.exceptions.ConnectionError:
        raise Exception("Connection Error")


def test_rpc_capabilities(endpoint):
    """Test RPC capabilities"""

    print(f"\n🔍 RPC Capability Test: {endpoint}")
    print("-" * 50)

    tests = [
        ("getHealth", [], "Basic connection"),
        ("getVersion", [], "Version info"),
        ("getSlot", [], "Current slot"),
        ("getTokenSupply", [ROACORE_TOKEN_MINT], "Token supply"),
        ("getTokenLargestAccounts", [ROACORE_TOKEN_MINT], "Largest accounts")
    ]

    results = {}

    for method, params, description in tests:
        try:
            print(f"   Testing: {description} ({method})")
            result, response_time = call_solana_rpc_with_timing(
                endpoint, method, params, timeout=30
            )
            results[method] = {
                'success': True,
                'response_time': response_time,
                'data_size': len(str(result)) if result else 0
            }
            print(f"   ✅ Success (Data size: {results[method]['data_size']} bytes)")

        except Exception as e:
            results[method] = {
                'success': False,
                'error': str(e),
                'response_time': None
            }
            print(f"   ❌ Failed: {e}")

    return results


def get_token_supply_enhanced(endpoint, token_mint):
    """Enhanced token supply query"""

    print("Getting token supply...")
    result, response_time = call_solana_rpc_with_timing(
        endpoint, "getTokenSupply", [token_mint], timeout=60
    )
    return result, response_time


def get_token_largest_accounts_enhanced(endpoint, token_mint):
    """Enhanced largest token accounts query (multiple methods)"""

    methods = [
        # Method 1: Basic approach
        {
            "params": [token_mint],
            "description": "Basic method"
        },
        # Method 2: Specify commitment
        {
            "params": [token_mint, {"commitment": "confirmed"}],
            "description": "Confirmed commitment"
        },
        # Method 3: Commitment + encoding
        {
            "params": [token_mint, {"commitment": "finalized", "encoding": "jsonParsed"}],
            "description": "Finalized commitment + jsonParsed"
        }
    ]

    for method in methods:
        try:
            print(f"Attempting largest accounts query: {method['description']}")
            result, response_time = call_solana_rpc_with_timing(
                endpoint, "getTokenLargestAccounts", method['params'], timeout=60
            )
            print(f"   ✅ {method['description']} success")
            return result, response_time

        except Exception as e:
            print(f"   ❌ {method['description']} failed: {e}")
            # Wait before trying next method
            time.sleep(2)
            continue

    raise Exception("All methods failed")


def analyze_token_enhanced(token_mint):
    """Enhanced token analysis (with RPC testing)"""

    endpoints = [
        {
            "url": "https://api.mainnet-beta.solana.com",
            "name": "Solana Official RPC",
            "type": "Public"
        },
        {
            "url": "https://rpc.ankr.com/solana",
            "name": "Ankr RPC",
            "type": "Public"
        },
        # QuickNode is private info, so commented out
        # {
        #     "url": "https://your-quicknode-url.com/",
        #     "name": "QuickNode",
        #     "type": "Premium"
        # }
    ]

    for endpoint_info in endpoints:
        endpoint = endpoint_info["url"]
        print(f"\n{'=' * 60}")
        print(f"🔄 Trying: {endpoint_info['name']} ({endpoint_info['type']})")
        print(f"URL: {endpoint}")
        print(f"{'=' * 60}")

        # 1. Test RPC capabilities
        capabilities = test_rpc_capabilities(endpoint)

        # 2. Attempt token analysis (only if capability test succeeded)
        if capabilities.get('getTokenSupply', {}).get('success') and \
                capabilities.get('getTokenLargestAccounts', {}).get('success'):

            try:
                print(f"\n📊 Starting token analysis...")

                # Get token supply
                supply_info, supply_time = get_token_supply_enhanced(endpoint, token_mint)
                decimals = supply_info['value']['decimals']
                total_supply = float(supply_info['value']['amount']) / (10 ** decimals)

                print(f"Total supply: {total_supply:,.2f} ROA")
                print(f"Decimals: {decimals}")

                # Get largest accounts
                largest_accounts, accounts_time = get_token_largest_accounts_enhanced(endpoint, token_mint)

                holders = []
                for account in largest_accounts['value']:
                    balance = float(account['amount']) / (10 ** decimals)
                    holders.append({
                        'address': account['address'],
                        'balance': balance
                    })

                print(f"\n✅ Success: {endpoint_info['name']}")
                print(f"📈 Performance info:")
                print(f"   - Token supply query: {supply_time:.2f}s")
                print(f"   - Largest accounts query: {accounts_time:.2f}s")
                print(f"   - Total time: {supply_time + accounts_time:.2f}s")

                return {
                    'holders': holders,
                    'total_supply': total_supply,
                    'decimals': decimals,
                    'success': True,
                    'endpoint_info': endpoint_info,
                    'performance': {
                        'supply_time': supply_time,
                        'accounts_time': accounts_time,
                        'total_time': supply_time + accounts_time
                    }
                }

            except Exception as e:
                print(f"❌ Token analysis failed: {e}")

        else:
            print(f"❌ Required RPC methods not supported")

        # Wait before trying next endpoint
        print(f"\n⏱️  Waiting 3 seconds before next endpoint...")
        time.sleep(3)

    return {'success': False, 'error': 'All endpoints failed'}


if __name__ == "__main__":
    print("ROA CORE Token Analysis (Advanced Diagnostics)")
    print(f"Token address: {ROACORE_TOKEN_MINT}")
    print(f"Analysis start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    result = analyze_token_enhanced(ROACORE_TOKEN_MINT)

    if result['success']:
        holders = result['holders']
        perf = result['performance']
        endpoint_info = result['endpoint_info']

        print(f"\n🏆 Analysis complete - Using {endpoint_info['name']}")
        print("=" * 60)

        for i, holder in enumerate(holders[:5], 1):
            print(f"{i}. Address: {holder['address']}")
            print(f"   Balance: {holder['balance']:,.6f} ROA")
            print("-" * 60)

        # Statistics
        top5_balance = sum(h['balance'] for h in holders[:5])
        percentage = (top5_balance / result['total_supply']) * 100

        print(f"\n📊 Statistics")
        print(f"   Top 5 holders total balance: {top5_balance:,.2f} ROA")
        print(f"   Percentage of total supply: {percentage:.2f}%")
        print(f"   RPC used: {endpoint_info['name']} ({endpoint_info['type']})")
        print(f"   Total response time: {perf['total_time']:.2f}s")

        # JSON output
        print(f"\n📋 JSON format:")
        print(json.dumps(holders[:5], indent=2, ensure_ascii=False))

    else:
        print(f"\n❌ Analysis failed: {result['error']}")
        print("\n💡 Recommendations:")
        print("1. Use premium RPC services (QuickNode, Alchemy)")
        print("2. Increase delay time to avoid rate limiting")
        print("3. Manual check: https://solscan.io/token/5tB5D6DGJMxxHYmNkfJNG237x6pZGEwTzGpUUh62yQJ7")