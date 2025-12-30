# token_stats_advanced_en.py
import requests
import json
import time
import csv
from datetime import datetime
import argparse
import os

ROACORE_TOKEN_MINT = "5tB5D6DGJMxxHYmNkfJNG237x6pZGEwTzGpUUh62yQJ7"

# Configuration
CONFIG = {
    "default_timeout": 60,
    "retry_delay": 3,
    "max_retries": 3,
    "output_dir": "output",
    "enable_logging": True
}


def setup_output_directory():
    """Create output directory if it doesn't exist"""
    if not os.path.exists(CONFIG["output_dir"]):
        os.makedirs(CONFIG["output_dir"])
        print(f"Created output directory: {CONFIG['output_dir']}")


def log_message(message, log_type="INFO"):
    """Log messages with timestamp"""
    if CONFIG["enable_logging"]:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] [{log_type}] {message}")


def call_solana_rpc_with_timing(endpoint, method, params=None, timeout=None):
    """Call Solana RPC with response time measurement and retry logic"""

    if timeout is None:
        timeout = CONFIG["default_timeout"]

    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": method
    }

    if params:
        payload["params"] = params

    for attempt in range(CONFIG["max_retries"]):
        start_time = time.time()

        try:
            log_message(f"Calling {method} (attempt {attempt + 1}/{CONFIG['max_retries']})")
            response = requests.post(endpoint, json=payload, timeout=timeout)
            end_time = time.time()
            response_time = end_time - start_time

            print(f"   Response time: {response_time:.2f}s")

            if response.status_code == 200:
                result = response.json()
                if 'error' in result:
                    error_details = result['error']
                    if attempt < CONFIG["max_retries"] - 1:
                        log_message(f"RPC Error (retrying): {error_details}", "WARNING")
                        time.sleep(CONFIG["retry_delay"])
                        continue
                    else:
                        raise Exception(f"RPC Error: {error_details}")
                return result['result'], response_time
            else:
                if attempt < CONFIG["max_retries"] - 1:
                    log_message(f"HTTP Error {response.status_code} (retrying)", "WARNING")
                    time.sleep(CONFIG["retry_delay"])
                    continue
                else:
                    raise Exception(f"HTTP Error: {response.status_code}")

        except requests.exceptions.Timeout:
            end_time = time.time()
            response_time = end_time - start_time
            if attempt < CONFIG["max_retries"] - 1:
                log_message(f"Timeout after {response_time:.2f}s (retrying)", "WARNING")
                time.sleep(CONFIG["retry_delay"])
                continue
            else:
                raise Exception(f"Timeout after {response_time:.2f} seconds")
        except requests.exceptions.ConnectionError:
            if attempt < CONFIG["max_retries"] - 1:
                log_message("Connection error (retrying)", "WARNING")
                time.sleep(CONFIG["retry_delay"])
                continue
            else:
                raise Exception("Connection Error")


def get_token_metadata(endpoint, token_mint):
    """Get comprehensive token metadata"""

    log_message("Fetching token metadata...")

    try:
        # Get token supply
        supply_result, supply_time = call_solana_rpc_with_timing(
            endpoint, "getTokenSupply", [token_mint]
        )

        # Get account info for additional metadata
        account_result, account_time = call_solana_rpc_with_timing(
            endpoint, "getAccountInfo", [token_mint, {"encoding": "jsonParsed"}]
        )

        metadata = {
            "mint_address": token_mint,
            "decimals": supply_result['value']['decimals'],
            "total_supply": float(supply_result['value']['amount']) / (10 ** supply_result['value']['decimals']),
            "supply_query_time": supply_time,
            "account_query_time": account_time,
            "timestamp": datetime.now().isoformat()
        }

        # Try to extract additional info from account data
        if account_result and 'data' in account_result['value']:
            account_data = account_result['value']['data']
            if isinstance(account_data, dict) and 'parsed' in account_data:
                parsed_data = account_data['parsed']
                if 'info' in parsed_data:
                    info = parsed_data['info']
                    metadata.update({
                        "mint_authority": info.get('mintAuthority'),
                        "freeze_authority": info.get('freezeAuthority'),
                        "is_initialized": info.get('isInitialized', False)
                    })

        return metadata

    except Exception as e:
        log_message(f"Failed to get complete metadata: {e}", "ERROR")
        # Return basic metadata
        supply_result, supply_time = call_solana_rpc_with_timing(
            endpoint, "getTokenSupply", [token_mint]
        )
        return {
            "mint_address": token_mint,
            "decimals": supply_result['value']['decimals'],
            "total_supply": float(supply_result['value']['amount']) / (10 ** supply_result['value']['decimals']),
            "supply_query_time": supply_time,
            "timestamp": datetime.now().isoformat()
        }


def get_token_holders_comprehensive(endpoint, token_mint, top_n=20):
    """Get comprehensive token holder information"""

    log_message(f"Fetching top {top_n} token holders...")

    methods = [
        {
            "params": [token_mint],
            "description": "Basic method"
        },
        {
            "params": [token_mint, {"commitment": "confirmed"}],
            "description": "Confirmed commitment"
        },
        {
            "params": [token_mint, {"commitment": "finalized"}],
            "description": "Finalized commitment"
        }
    ]

    for method in methods:
        try:
            log_message(f"Attempting: {method['description']}")
            result, response_time = call_solana_rpc_with_timing(
                endpoint, "getTokenLargestAccounts", method['params']
            )

            log_message(f"✅ {method['description']} succeeded in {response_time:.2f}s")
            return result, response_time, method['description']

        except Exception as e:
            log_message(f"❌ {method['description']} failed: {e}", "WARNING")
            time.sleep(2)
            continue

    raise Exception("All holder query methods failed")


def calculate_holder_statistics(holders, total_supply):
    """Calculate comprehensive holder statistics"""

    if not holders:
        return {}

    balances = [h['balance'] for h in holders]

    stats = {
        "total_holders_analyzed": len(holders),
        "top_5_balance": sum(balances[:5]),
        "top_10_balance": sum(balances[:10]) if len(balances) >= 10 else sum(balances),
        "top_20_balance": sum(balances[:20]) if len(balances) >= 20 else sum(balances),
        "largest_holder_balance": max(balances) if balances else 0,
        "smallest_analyzed_balance": min(balances) if balances else 0,
        "average_balance": sum(balances) / len(balances) if balances else 0,
        "median_balance": sorted(balances)[len(balances) // 2] if balances else 0
    }

    # Calculate percentages
    if total_supply > 0:
        stats.update({
            "top_5_percentage": (stats["top_5_balance"] / total_supply) * 100,
            "top_10_percentage": (stats["top_10_balance"] / total_supply) * 100,
            "top_20_percentage": (stats["top_20_balance"] / total_supply) * 100,
            "largest_holder_percentage": (stats["largest_holder_balance"] / total_supply) * 100
        })

    return stats


def export_to_csv(holders, metadata, stats, filename=None):
    """Export results to CSV file"""

    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{CONFIG['output_dir']}/roa_holders_{timestamp}.csv"

    try:
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)

            # Write metadata
            writer.writerow(["# ROA CORE Token Holder Analysis"])
            writer.writerow(["# Generated:", metadata.get('timestamp', 'Unknown')])
            writer.writerow(["# Token Address:", metadata.get('mint_address', 'Unknown')])
            writer.writerow(["# Total Supply:", f"{metadata.get('total_supply', 0):,.2f}"])
            writer.writerow([])

            # Write statistics
            writer.writerow(["# Statistics"])
            for key, value in stats.items():
                if isinstance(value, float):
                    writer.writerow([f"# {key}:", f"{value:.6f}"])
                else:
                    writer.writerow([f"# {key}:", value])
            writer.writerow([])

            # Write headers
            writer.writerow(["Rank", "Address", "Balance", "Percentage"])

            # Write holder data
            total_supply = metadata.get('total_supply', 0)
            for i, holder in enumerate(holders, 1):
                percentage = (holder['balance'] / total_supply * 100) if total_supply > 0 else 0
                writer.writerow([
                    i,
                    holder['address'],
                    f"{holder['balance']:.6f}",
                    f"{percentage:.4f}%"
                ])

        log_message(f"Data exported to: {filename}")
        return filename

    except Exception as e:
        log_message(f"Failed to export CSV: {e}", "ERROR")
        return None


def export_to_json(data, filename=None):
    """Export results to JSON file"""

    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{CONFIG['output_dir']}/roa_analysis_{timestamp}.json"

    try:
        with open(filename, 'w', encoding='utf-8') as jsonfile:
            json.dump(data, jsonfile, indent=2, ensure_ascii=False)

        log_message(f"Data exported to: {filename}")
        return filename

    except Exception as e:
        log_message(f"Failed to export JSON: {e}", "ERROR")
        return None


def analyze_token_comprehensive(token_mint, top_n=20, export_csv=False, export_json=False):
    """Comprehensive token analysis with all features"""

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
        }
        # Add your premium RPC here
        # {
        #     "url": "https://your-premium-rpc-url.com/",
        #     "name": "Premium RPC",
        #     "type": "Premium"
        # }
    ]

    for endpoint_info in endpoints:
        endpoint = endpoint_info["url"]
        log_message(f"Trying: {endpoint_info['name']} ({endpoint_info['type']})")
        log_message(f"URL: {endpoint}")

        try:
            # Get token metadata
            metadata = get_token_metadata(endpoint, token_mint)

            # Get holder information
            largest_accounts, accounts_time, method_used = get_token_holders_comprehensive(
                endpoint, token_mint, top_n
            )

            # Process holder data
            holders = []
            for account in largest_accounts['value']:
                balance = float(account['amount']) / (10 ** metadata['decimals'])
                holders.append({
                    'address': account['address'],
                    'balance': balance
                })

            # Calculate statistics
            stats = calculate_holder_statistics(holders, metadata['total_supply'])

            # Prepare comprehensive result
            result = {
                'success': True,
                'metadata': metadata,
                'holders': holders,
                'statistics': stats,
                'endpoint_info': endpoint_info,
                'method_used': method_used,
                'query_time': accounts_time,
                'analysis_timestamp': datetime.now().isoformat()
            }

            log_message(f"✅ Analysis completed using {endpoint_info['name']}")
            log_message(f"Total query time: {accounts_time:.2f}s")
            log_message(f"Method used: {method_used}")

            # Export data if requested
            if export_csv:
                csv_file = export_to_csv(holders, metadata, stats)
                result['csv_export'] = csv_file

            if export_json:
                json_file = export_to_json(result)
                result['json_export'] = json_file

            return result

        except Exception as e:
            log_message(f"❌ Failed with {endpoint_info['name']}: {e}", "ERROR")
            log_message("Waiting before trying next endpoint...", "INFO")
            time.sleep(3)
            continue

    return {'success': False, 'error': 'All endpoints failed'}


def print_analysis_report(result):
    """Print comprehensive analysis report"""

    if not result['success']:
        print(f"\n❌ Analysis failed: {result['error']}")
        print("\n💡 Recommendations:")
        print("1. Use premium RPC services (QuickNode, Alchemy)")
        print("2. Check network connectivity")
        print("3. Try again later")
        return

    metadata = result['metadata']
    holders = result['holders']
    stats = result['statistics']
    endpoint_info = result['endpoint_info']

    print(f"\n🏆 ROA CORE Token Analysis Complete")
    print("=" * 80)

    # Token Information
    print(f"\n📊 Token Information")
    print(f"   Address: {metadata['mint_address']}")
    print(f"   Total Supply: {metadata['total_supply']:,.2f} ROA")
    print(f"   Decimals: {metadata['decimals']}")
    print(f"   Analysis Time: {metadata['timestamp']}")

    # RPC Information
    print(f"\n🌐 RPC Information")
    print(f"   Provider: {endpoint_info['name']} ({endpoint_info['type']})")
    print(f"   Method Used: {result['method_used']}")
    print(f"   Query Time: {result['query_time']:.2f}s")

    # Top Holders
    print(f"\n🥇 Top {min(10, len(holders))} Holders")
    print("-" * 80)
    for i, holder in enumerate(holders[:10], 1):
        percentage = (holder['balance'] / metadata['total_supply']) * 100
        print(f"{i:2d}. {holder['address']}")
        print(f"    Balance: {holder['balance']:,.6f} ROA ({percentage:.4f}%)")
        print("-" * 80)

    # Statistics
    print(f"\n📈 Holder Statistics")
    print(f"   Top 5 Holdings: {stats['top_5_balance']:,.2f} ROA ({stats.get('top_5_percentage', 0):.2f}%)")
    print(f"   Top 10 Holdings: {stats['top_10_balance']:,.2f} ROA ({stats.get('top_10_percentage', 0):.2f}%)")
    print(f"   Top 20 Holdings: {stats['top_20_balance']:,.2f} ROA ({stats.get('top_20_percentage', 0):.2f}%)")
    print(
        f"   Largest Holder: {stats['largest_holder_balance']:,.6f} ROA ({stats.get('largest_holder_percentage', 0):.4f}%)")
    print(f"   Average Balance: {stats['average_balance']:,.6f} ROA")
    print(f"   Median Balance: {stats['median_balance']:,.6f} ROA")

    # Export Information
    if 'csv_export' in result and result['csv_export']:
        print(f"\n📁 CSV exported to: {result['csv_export']}")
    if 'json_export' in result and result['json_export']:
        print(f"📁 JSON exported to: {result['json_export']}")


def main():
    """Main function with command line argument support"""

    parser = argparse.ArgumentParser(description='ROA CORE Token Holder Analysis')
    parser.add_argument('--top', type=int, default=20, help='Number of top holders to analyze (default: 20)')
    parser.add_argument('--csv', action='store_true', help='Export results to CSV file')
    parser.add_argument('--json', action='store_true', help='Export results to JSON file')
    parser.add_argument('--quiet', action='store_true', help='Reduce log output')
    parser.add_argument('--timeout', type=int, default=60, help='Request timeout in seconds (default: 60)')

    args = parser.parse_args()

    # Update configuration
    if args.quiet:
        CONFIG["enable_logging"] = False
    CONFIG["default_timeout"] = args.timeout

    # Setup
    setup_output_directory()

    print("ROA CORE Token Comprehensive Analysis")
    print(f"Token address: {ROACORE_TOKEN_MINT}")
    print(f"Analysis start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Analyzing top {args.top} holders")
    if args.csv:
        print("✓ CSV export enabled")
    if args.json:
        print("✓ JSON export enabled")

    # Run analysis
    result = analyze_token_comprehensive(
        ROACORE_TOKEN_MINT,
        top_n=args.top,
        export_csv=args.csv,
        export_json=args.json
    )

    # Print report
    print_analysis_report(result)


if __name__ == "__main__":
    main()