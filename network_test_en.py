# network_test_en.py
import requests
import time


def test_rpc_endpoints():
    """Test connections to various RPC endpoints"""

    endpoints = [
        "https://api.mainnet-beta.solana.com"
    ]

    print("Solana RPC Endpoint Connection Test")
    print("=" * 60)

    for endpoint in endpoints:
        try:
            print(f"Testing: {endpoint}")

            # Simple getHealth request
            response = requests.post(
                endpoint,
                json={
                    "jsonrpc": "2.0",
                    "id": 1,
                    "method": "getHealth"
                },
                timeout=10
            )

            if response.status_code == 200:
                result = response.json()
                print(f"✅ Success - Response: {result}")
            else:
                print(f"❌ HTTP Error: {response.status_code}")

        except requests.exceptions.Timeout:
            print(f"❌ Timeout: {endpoint}")
        except requests.exceptions.ConnectionError:
            print(f"❌ Connection Error: {endpoint}")
        except Exception as e:
            print(f"❌ Other Error: {e}")

        print("-" * 60)
        time.sleep(1)


if __name__ == "__main__":
    test_rpc_endpoints()
