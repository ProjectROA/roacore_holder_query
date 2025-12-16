# token_stats_enhanced.py
import requests
import json
import time
from datetime import datetime

ROACORE_TOKEN_MINT = "5tB5D6DGJMxxHYmNkfJNG237x6pZGEwTzGpUUh62yQJ7"


def call_solana_rpc_with_timing(endpoint, method, params=None, timeout=60):
    """응답 시간 측정과 함께 Solana RPC 호출"""

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

        print(f"   응답 시간: {response_time:.2f}초")

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
    """RPC 기능 테스트"""

    print(f"\n🔍 RPC 기능 테스트: {endpoint}")
    print("-" * 50)

    tests = [
        ("getHealth", [], "기본 연결"),
        ("getVersion", [], "버전 정보"),
        ("getSlot", [], "현재 슬롯"),
        ("getTokenSupply", [ROACORE_TOKEN_MINT], "토큰 공급량"),
        ("getTokenLargestAccounts", [ROACORE_TOKEN_MINT], "대형 계정")
    ]

    results = {}

    for method, params, description in tests:
        try:
            print(f"   테스트: {description} ({method})")
            result, response_time = call_solana_rpc_with_timing(
                endpoint, method, params, timeout=30
            )
            results[method] = {
                'success': True,
                'response_time': response_time,
                'data_size': len(str(result)) if result else 0
            }
            print(f"   ✅ 성공 (데이터 크기: {results[method]['data_size']} bytes)")

        except Exception as e:
            results[method] = {
                'success': False,
                'error': str(e),
                'response_time': None
            }
            print(f"   ❌ 실패: {e}")

    return results


def get_token_supply_enhanced(endpoint, token_mint):
    """개선된 토큰 공급량 조회"""

    print("토큰 공급량 조회 중...")
    result, response_time = call_solana_rpc_with_timing(
        endpoint, "getTokenSupply", [token_mint], timeout=60
    )
    return result, response_time


def get_token_largest_accounts_enhanced(endpoint, token_mint):
    """개선된 토큰 대형 계정 조회 (여러 방법 시도)"""

    methods = [
        # 방법 1: 기본적인 방법
        {
            "params": [token_mint],
            "description": "기본 방법"
        },
        # 방법 2: commitment 지정
        {
            "params": [token_mint, {"commitment": "confirmed"}],
            "description": "confirmed commitment"
        },
        # 방법 3: commitment + encoding 지정
        {
            "params": [token_mint, {"commitment": "finalized", "encoding": "jsonParsed"}],
            "description": "finalized commitment + jsonParsed"
        }
    ]

    for method in methods:
        try:
            print(f"대형 계정 조회 시도: {method['description']}")
            result, response_time = call_solana_rpc_with_timing(
                endpoint, "getTokenLargestAccounts", method['params'], timeout=60
            )
            print(f"   ✅ {method['description']} 성공")
            return result, response_time

        except Exception as e:
            print(f"   ❌ {method['description']} 실패: {e}")
            # 다음 방법 시도를 위해 잠시 대기
            time.sleep(2)
            continue

    raise Exception("모든 방법 실패")


def analyze_token_enhanced(token_mint):
    """개선된 토큰 분석 (RPC 테스트 포함)"""

    endpoints = [
        {
            "url": "https://api.mainnet-beta.solana.com",
            "name": "Solana 공식 RPC",
            "type": "공개"
        },
        {
            "url": "https://rpc.ankr.com/solana",
            "name": "Ankr RPC",
            "type": "공개"
        },
        # QuickNode는 개인 정보이므로 주석 처리
        # {
        #     "url": "https://your-quicknode-url.com/",
        #     "name": "QuickNode",
        #     "type": "프리미엄"
        # }
    ]

    for endpoint_info in endpoints:
        endpoint = endpoint_info["url"]
        print(f"\n{'=' * 60}")
        print(f"🔄 시도 중: {endpoint_info['name']} ({endpoint_info['type']})")
        print(f"URL: {endpoint}")
        print(f"{'=' * 60}")

        # 1. RPC 기능 테스트
        capabilities = test_rpc_capabilities(endpoint)

        # 2. 토큰 분석 시도 (기능 테스트에서 성공한 경우만)
        if capabilities.get('getTokenSupply', {}).get('success') and \
                capabilities.get('getTokenLargestAccounts', {}).get('success'):

            try:
                print(f"\n📊 토큰 분석 시작...")

                # 토큰 공급량 조회
                supply_info, supply_time = get_token_supply_enhanced(endpoint, token_mint)
                decimals = supply_info['value']['decimals']
                total_supply = float(supply_info['value']['amount']) / (10 ** decimals)

                print(f"총 공급량: {total_supply:,.2f} ROA")
                print(f"Decimals: {decimals}")

                # 대형 계정 조회
                largest_accounts, accounts_time = get_token_largest_accounts_enhanced(endpoint, token_mint)

                holders = []
                for account in largest_accounts['value']:
                    balance = float(account['amount']) / (10 ** decimals)
                    holders.append({
                        'address': account['address'],
                        'balance': balance
                    })

                print(f"\n✅ 성공: {endpoint_info['name']}")
                print(f"📈 성능 정보:")
                print(f"   - 토큰 공급량 조회: {supply_time:.2f}초")
                print(f"   - 대형 계정 조회: {accounts_time:.2f}초")
                print(f"   - 총 소요 시간: {supply_time + accounts_time:.2f}초")

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
                print(f"❌ 토큰 분석 실패: {e}")

        else:
            print(f"❌ 필수 RPC 메서드 지원 안함")

        # 다음 엔드포인트 시도 전 대기
        print(f"\n⏱️  다음 엔드포인트 시도까지 3초 대기...")
        time.sleep(3)

    return {'success': False, 'error': '모든 엔드포인트 실패'}


if __name__ == "__main__":
    print("ROA CORE 토큰 분석 (고급 진단 포함)")
    print(f"토큰 주소: {ROACORE_TOKEN_MINT}")
    print(f"분석 시작 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    result = analyze_token_enhanced(ROACORE_TOKEN_MINT)

    if result['success']:
        holders = result['holders']
        perf = result['performance']
        endpoint_info = result['endpoint_info']

        print(f"\n🏆 분석 완료 - {endpoint_info['name']} 사용")
        print("=" * 60)

        for i, holder in enumerate(holders[:5], 1):
            print(f"{i}. 주소: {holder['address']}")
            print(f"   잔액: {holder['balance']:,.6f} ROA")
            print("-" * 60)

        # 통계
        top5_balance = sum(h['balance'] for h in holders[:5])
        percentage = (top5_balance / result['total_supply']) * 100

        print(f"\n📊 통계")
        print(f"   상위 5개 홀더 총 잔액: {top5_balance:,.2f} ROA")
        print(f"   전체 공급량 대비: {percentage:.2f}%")
        print(f"   사용된 RPC: {endpoint_info['name']} ({endpoint_info['type']})")
        print(f"   총 응답 시간: {perf['total_time']:.2f}초")

        # JSON 출력
        print(f"\n📋 JSON 형태:")
        print(json.dumps(holders[:5], indent=2, ensure_ascii=False))

    else:
        print(f"\n❌ 분석 실패: {result['error']}")
        print("\n💡 권장사항:")
        print("1. 프리미엄 RPC 서비스 (QuickNode, Alchemy) 사용")
        print("2. Rate limiting 회피를 위한 지연 시간 증가")
        print("3. 수동 확인: https://solscan.io/token/5tB5D6DGJMxxHYmNkfJNG237x6pZGEwTzGpUUh62yQJ7")