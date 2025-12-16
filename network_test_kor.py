# network_test.py
import requests
import time


def test_rpc_endpoints():
    """다양한 RPC 엔드포인트 연결 테스트"""

    endpoints = [
        "https://api.mainnet-beta.solana.com"
    ]

    print("Solana RPC 엔드포인트 연결 테스트")
    print("=" * 60)

    for endpoint in endpoints:
        try:
            print(f"테스트: {endpoint}")

            # 간단한 getHealth 요청
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
                print(f"✅ 성공 - 응답: {result}")
            else:
                print(f"❌ HTTP 오류: {response.status_code}")

        except requests.exceptions.Timeout:
            print(f"❌ 타임아웃: {endpoint}")
        except requests.exceptions.ConnectionError:
            print(f"❌ 연결 오류: {endpoint}")
        except Exception as e:
            print(f"❌ 기타 오류: {e}")

        print("-" * 60)
        time.sleep(1)


if __name__ == "__main__":
    test_rpc_endpoints()