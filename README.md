# ROA CORE Token Analysis Tools

ROA CORE 토큰의 상위 홀더를 조회하고 분석하는 Python 스크립트 모음입니다.

A collection of Python scripts for querying and analyzing top holders of the ROA CORE token.

## 🎯 개요 / Overview

이 프로젝트는 Solana 블록체인의 ROA CORE 토큰(`5tB5D6DGJMxxHYmNkfJNG237x6pZGEwTzGpUUh62yQJ7`)의 상위 홀더 정보를 조회하고 분석하는 도구들을 제공합니다.

This project provides tools for querying and analyzing top holder information for the ROA CORE token (`5tB5D6DGJMxxHYmNkfJNG237x6pZGEwTzGpUUh62yQJ7`) on the Solana blockchain.

## 📁 파일 구조 / File Structure

```
├── network_test.py                 # 한국어 - RPC 연결 테스트
├── network_test_en.py             # English - RPC connection test
├── roacore_holder_query_kor.py    # 한국어 - 토큰 상위 홀더 조회
└── README.md                      # 프로젝트 설명서
```

## 🔧 요구사항 / Requirements

### Python 버전 / Python Version

- Python 3.11+ 권장 / Python 3.11+ recommended

### 필수 패키지 / Required Packages

```bash
pip install requests
```

## 🚀 설치 및 실행 / Installation & Usage

### 1. 가상환경 생성 / Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python -m venv venv
source venv/bin/activate
```

### 2. 패키지 설치 / Install Packages

```bash
pip install requests
```

### 3. 스크립트 실행 / Run Scripts

```bash
# RPC 연결 테스트 / RPC Connection Test
python network_test_en.py           # English version
python network_test_kor.py          # Korean version


# 기본 토큰 분석 / Basic Token Analysis
python tokenstats.py          # English version
python tokenstats_kor.py      # Korean version


# 고급 진단 분석 / Advanced Diagnostics Analysis
# python token_stats_enhanced.py          # English version
# python token_stats_enhanced_kor.py      # Korean version
```

## 📊 스크립트 설명 / Script Descriptions

### 1. 네트워크 테스트 / Network Test (`network_test.py`)

**목적 / Purpose:** Solana RPC 엔드포인트의 기본 연결 상태를 확인

**기능 / Features:**

- RPC 엔드포인트 연결 테스트
- `getHealth` API 호출을 통한 기본 상태 확인
- 응답 시간 및 오류 처리

**사용 사례 / Use Case:** RPC 서비스가 정상 작동하는지 확인할 때

### 2. 기본 토큰 분석 / Basic Token Analysis (`tokenstats.py`)

**목적 / Purpose:** ROA CORE 토큰의 상위 홀더 정보를 조회

**기능 / Features:**

- 토큰 총 공급량 조회
- 상위 대형 계정 홀더 목록
- 홀더별 잔액 및 비율 계산
- JSON 형태 결과 출력

**출력 예시 / Sample Output:**

```
🏆 상위 홀더 목록
============================================================
1. 주소: ABC123...XYZ789
   잔액: 1,234,567.890000 ROA
------------------------------------------------------------
📊 상위 5개 홀더 총 잔액: 12,345,678.90 ROA
🎯 전체 공급량 대비: 15.67%
```

### 3. 고급 진단 분석 / Advanced Diagnostics Analysis (`token_stats_enhanced.py`)

**목적 / Purpose:** 종합적인 RPC 성능 분석과 토큰 데이터 조회

**고급 기능 / Advanced Features:**

- **RPC 기능 테스트**: 각 엔드포인트의 지원 메서드 확인
- **응답 시간 측정**: 정확한 성능 분석
- **다중 방법 시도**: 여러 파라미터 조합으로 재시도
- **자동 엔드포인트 선택**: 가장 안정적인 RPC 자동 선택
- **상세 성능 리포트**: 총 소요 시간, 데이터 크기 등

**성능 분석 예시 / Performance Analysis Example:**

```
🔍 RPC 기능 테스트: https://api.mainnet-beta.solana.com
   테스트: 기본 연결 (getHealth)
   응답 시간: 0.45초
   ✅ 성공 (데이터 크기: 156 bytes)

📈 성능 정보:
   - 토큰 공급량 조회: 1.23초
   - 대형 계정 조회: 2.45초
   - 총 소요 시간: 3.68초
```

## 🌐 지원하는 RPC 엔드포인트 / Supported RPC Endpoints

### 공개 RPC / Public RPCs

- **Solana 공식 / Official:** `https://api.mainnet-beta.solana.com`
- **Ankr:** `https://rpc.ankr.com/solana`

### 프리미엄 RPC / Premium RPCs

- **QuickNode:** 개인 URL 필요 / Personal URL required
- **Alchemy:** 개인 API 키 필요 / Personal API key required
- **Helius:** 개인 API 키 필요 / Personal API key required

## ⚠️ 주의사항 / Important Notes

### RPC 제한사항 / RPC Limitations

1. **공개 RPC 제한 / Public RPC Limitations:**

   - Rate limiting (분당 요청 수 제한)
   - 일부 고급 메서드 지원 안함
   - 느린 응답 시간 (5-30초)
   - 가끔씩 서비스 중단

2. **프리미엄 RPC 장점 / Premium RPC Benefits:**
   - 높은 요청 한도
   - 모든 RPC 메서드 지원
   - 빠른 응답 시간 (1-3초)
   - 안정적인 서비스

### 성능 최적화 권장사항 / Performance Optimization Recommendations

1. **프리미엄 RPC 사용 / Use Premium RPC**

   ```python
   # QuickNode 예시 / QuickNode example
   endpoints = [
       "https://your-quicknode-endpoint.quiknode.pro/your-api-key/"
   ]
   ```

2. **적절한 타임아웃 설정 / Set Appropriate Timeouts**

   ```python
   response = requests.post(endpoint, json=payload, timeout=60)
   ```

3. **요청 간 지연 추가 / Add Delays Between Requests**
   ```python
   time.sleep(2)  # 2초 대기
   ```

## 🔍 문제 해결 / Troubleshooting

### 일반적인 오류 / Common Errors

1. **`AttributeError: 'dict' object has no attribute 'offset'`**

   - **원인 / Cause:** solana 라이브러리 버전 호환성 문제
   - **해결책 / Solution:** `tokenstats.py` 사용 (순수 requests 방식)

2. **`Timeout Error`**

   - **원인 / Cause:** RPC 응답 지연
   - **해결책 / Solution:** 타임아웃 값 증가 또는 프리미엄 RPC 사용

3. **`RPC Error: Method not found`**

   - **원인 / Cause:** 해당 RPC가 특정 메서드를 지원하지 않음
   - **해결책 / Solution:** 다른 RPC 엔드포인트 시도

4. **`Rate limiting`**
   - **원인 / Cause:** 요청 한도 초과
   - **해결책 / Solution:** 요청 간 지연 시간 추가

## 📈 분석 결과 활용 / Using Analysis Results

### JSON 데이터 구조 / JSON Data Structure

```json
[
  {
    "address": "홀더주소",
    "balance": 1234567.89
  },
  ...
]
```

### 데이터 활용 예시 / Data Usage Examples

```python
# 상위 홀더 비율 계산
top5_balance = sum(holder['balance'] for holder in holders[:5])
percentage = (top5_balance / total_supply) * 100

# 특정 잔액 이상 홀더 필터링
large_holders = [h for h in holders if h['balance'] > 100000]
```

## 🔗 유용한 링크 / Useful Links

### 블록체인 익스플로러 / Blockchain Explorers

- **Solscan:** https://solscan.io/token/5tB5D6DGJMxxHYmNkfJNG237x6pZGEwTzGpUUh62yQJ7
- **Solana Explorer:** https://explorer.solana.com/address/5tB5D6DGJMxxHYmNkfJNG237x6pZGEwTzGpUUh62yQJ7
- **SolanaFM:** https://solana.fm/address/5tB5D6DGJMxxHYmNkfJNG237x6pZGEwTzGpUUh62yQJ7

### RPC 서비스 / RPC Services

- **QuickNode:** https://www.quicknode.com/
- **Alchemy:** https://www.alchemy.com/
- **Helius:** https://helius.xyz/

## 🤝 기여 / Contributing

이 프로젝트에 기여하고 싶으시다면:

If you'd like to contribute to this project:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 라이선스 / License

이 프로젝트는 MIT 라이선스 하에 배포됩니다.

This project is distributed under the MIT License.

## ⚡ 빠른 시작 / Quick Start

```bash
# 1. 클론 및 설정 / Clone and setup
git clone <repository-url>
cd roa-token-analysis
python -m venv venv
venv\Scripts\activate  # Windows
pip install requests

# 2. 기본 분석 실행 / Run basic analysis
python tokenstats.py

# 3. 고급 분석 실행 / Run advanced analysis
python token_stats_enhanced.py
```

---

**마지막 업데이트 / Last Updated:** 2025-12-18
