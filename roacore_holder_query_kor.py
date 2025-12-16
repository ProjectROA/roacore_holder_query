# token_stats_requests.py
import requests
import json

ROACORE_TOKEN_MINT = "5tB5D6DGJMxxHYmNkfJNG237x6pZGEwTzGpUUh62yQJ7"


def call_solana_rpc(endpoint, method, params=None):
    """순수 requests로 Solana RPC 호출"""

    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": method
    }

    if params:
        payload["params"] = params

    response = requests.post(endpoint, json=payload, timeout=30)

    if response.status_code == 200:
        result = response.json()
        if 'error' in result:
            raise Exception(f"RPC Error: {result['error']}")
        return result['result']
    else:
        raise Exception(f"HTTP Error: {response.status_code}")


def get_token_supply_simple(endpoint, token_mint):
    """토큰 공급량 조회"""

    result = call_solana_rpc(endpoint, "getTokenSupply", [token_mint])
    return result


def get_token_largest_accounts_simple(endpoint, token_mint):
    """토큰 대형 계정 조회"""

    # commitment 옵션 추가
    params = [token_mint, {"commitment": "confirmed"}]
    result = call_solana_rpc(endpoint, "getTokenLargestAccounts", params)
    return result


def analyze_token_simple(token_mint):
    """순수 requests로 토큰 분석"""

    endpoints = [
        "https://api.mainnet-beta.solana.com"
    ]

    for endpoint in endpoints:
        print(f"시도 중: {endpoint}")

        try:
            # 1. 토큰 공급량 조회
            print("토큰 공급량 조회 중...")
            supply_info = get_token_supply_simple(endpoint, token_mint)
            decimals = supply_info['value']['decimals']
            total_supply = float(supply_info['value']['amount']) / (10 ** decimals)

            print(f"총 공급량: {total_supply:,.2f} ROA")
            print(f"Decimals: {decimals}")

            # 2. 대형 계정 조회
            print("대형 계정 조회 중...")
            largest_accounts = get_token_largest_accounts_simple(endpoint, token_mint)

            holders = []
            for account in largest_accounts['value']:
                balance = float(account['amount']) / (10 ** decimals)
                holders.append({
                    'address': account['address'],
                    'balance': balance
                })

            print(f"✅ 성공: {endpoint}")
            return {
                'holders': holders,
                'total_supply': total_supply,
                'decimals': decimals,
                'success': True
            }

        except Exception as e:
            print(f"❌ 실패: {endpoint}")
            print(f"오류: {e}")
            continue

    return {'success': False, 'error': '모든 엔드포인트 실패'}


if __name__ == "__main__":
    print("ROA CORE 토큰 분석 (순수 requests 방식)")
    print(f"토큰 주소: {ROACORE_TOKEN_MINT}")
    print("=" * 60)

    result = analyze_token_simple(ROACORE_TOKEN_MINT)

    if result['success']:
        holders = result['holders']

        print("\n🏆 상위 홀더 목록")
        print("=" * 60)

        for i, holder in enumerate(holders[:5], 1):
            print(f"{i}. 주소: {holder['address']}")
            print(f"   잔액: {holder['balance']:,.6f} ROA")
            print("-" * 60)

        # 통계
        top5_balance = sum(h['balance'] for h in holders[:5])
        percentage = (top5_balance / result['total_supply']) * 100

        print(f"\n📊 상위 5개 홀더 총 잔액: {top5_balance:,.2f} ROA")
        print(f"🎯 전체 공급량 대비: {percentage:.2f}%")

        # JSON 출력
        print(f"\n📋 JSON 형태:")
        print(json.dumps(holders[:5], indent=2, ensure_ascii=False))

    else:
        print(f"❌ 분석 실패: {result['error']}")
        print("\n💡 수동 확인 링크:")
        print("1. https://solscan.io/token/5tB5D6DGJMxxHYmNkfJNG237x6pZGEwTzGpUUh62yQJ7")