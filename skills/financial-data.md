# 재무 데이터 수집 및 교차 검증 규범

본 규범은 기업 재무 데이터가 관련된 모든 연구에 적용된다. **모든 핵심 데이터는 독립적인 두 출처에서 확보해야 하며, 오차가 1%를 넘으면 표시해야 한다.**

---

## 데이터 소스 우선순위

### 미국 주식（PDD, 텐센트 ADR, 넷이즈 ADR 등）

| 우선순위 | 출처 | URL | 확보 방식 |
|--------|------|-----|---------|
| 1（주） | **macrotrends** | macrotrends.net/stocks/charts/{ticker} | 직접 접속, 가입 불필요 |
| 2（부） | **stockanalysis** | stockanalysis.com/stocks/{ticker}/financials | 직접 접속, 가입 불필요 |
| 원본 1차 | SEC EDGAR | sec.gov/cgi-bin/browse-edgar | 10-K / 10-Q 원문 |

### 홍콩 주식（텐센트 0700, 넷이즈 9999, 메이퇀 3690 등）

| 우선순위 | 출처 | URL | 확보 방식 |
|--------|------|-----|---------|
| 1（주） | **aastocks** | aastocks.com/tc/stocks/analysis/company-fundamental | 직접 접속 |
| 2（부） | **macrotrends**（ADR 코드） | 텐센트는 TCEHY, 넷이즈는 NTES | 직접 접속 |
| 원본 1차 | HKEX 디스클로저（披露易） | hkexnews.hk | 연차보고서 PDF |

### A주（37인터랙티브엔터테인먼트, 지비트 등）

| 우선순위 | 출처 | URL | 확보 방식 |
|--------|------|-----|---------|
| 1（주） | **둥팡차이푸（东方财富）** | eastmoney.com → 종목 코드 검색 → 재무제표 | 직접 접속 |
| 2（부） | **쥐차오쯔쉰（巨潮资讯）** | cninfo.com.cn | 원본 연차/분기 보고서 PDF |
| 도구 | **ashare_data.py** | `py tools/ashare_data.py financials {코드}` | 자동 데이터 수집（텐센트 시세 + 둥팡차이푸） |

### 한국 주식 / 한국（KOSPI/KOSDAQ — 삼성전자 005930、카카오 035720 등）

| 优先级 | 来源 | URL | 获取方式 |
|--------|------|-----|---------|
| 1（主） | **krx_data.py（네이버 금융）** | `py tools/krx_data.py financials\|quote\|valuation\|search {코드}` | 自动取数，零依赖 |
| 2（副） | **네이버 금융** | finance.naver.com/item/main.naver?code={코드} | 直接访问 |
| 原始一手 | **DART 전자공시** | dart.fss.or.kr | 사업보고서/분기보고서 원문 |
| 行情/分类 | **KRX 정보데이터시스템** | data.krx.co.kr | 시세·업종분류·시가총액 |

> 韩股代码为 6 位数字。金额单位通常为 **억원(亿韩元)**，注意与 조원(만억원) 换算。
> ADR 가능 종목(예: 쿠팡 CPNG, 그랩 등 美상장)은 美股 来源(macrotrends/SEC) 우선.

---

## 실행 규범

### 1단계: 데이터 확보

각 재무 지표（매출, 순이익, 매출총이익률, 영업현금흐름, 부채비율 등）에 대해 **출처 1**과 **출처 2**에서 각각 데이터를 확보한다.

### 2단계: 오차 계산 및 표시

```
오차율 = |출처1 수치 - 출처2 수치| / 출처1 수치 × 100%
```

| 오차 | 처리 방식 |
|------|---------|
| 1% 이하 | ✅ 일치, 출처1 수치 채택, 두 출처 모두 표기 |
| 1% ~ 5% | ⚠️ "데이터 차이 존재" 표시, 두 수치 명기, 가능한 원인 설명（환율/회계 기준） |
| 5% 초과 | ❌ "데이터에 중대한 차이 존재" 표시, 반드시 원본 재무제표로 확인, 직접 사용 불가 |

### 3단계: 데이터 표기 형식

각 핵심 데이터는 아래 형식으로 표기해야 한다.

```
매출：1,239억 위안 ✅
  - macrotrends: 1,241억 위안
  - stockanalysis: 1,237억 위안
  - 오차: 0.3%
```

차이 예시:
```
순이익：245억 위안 ⚠️ 데이터 차이 존재
  - macrotrends: 245억 위안（GAAP）
  - stockanalysis: 278억 위안（Non-GAAP）
  - 오차: 13.5% — 원인: 회계 기준 차이（GAAP vs Non-GAAP）
```

---

## 흔한 차이 원인（반드시 데이터 오류인 것은 아님）

| 원인 | 설명 |
|------|------|
| GAAP vs Non-GAAP | 가장 흔함, 특히 이익류 데이터 |
| 환율 환산 | 홍콩달러/위안/달러 환산 시점이 다름 |
| 회계연도 정의 | 자연연도 vs 회계연도（예: 애플 회계연도는 10월 종료） |
| 연결 기준 | 소수주주 지분 포함 여부 |
| 데이터 갱신 지연 | 특정 플랫폼이 최신 분기 실적을 아직 반영하지 않음 |

---

## 특별 규칙

1. **비상장 기업**（미호요, 릴리스 등）: 1차 데이터 출처만 있을 경우 데이터 앞에 `[추정]` 표기, 교차 검증은 수행하지 않음
2. **분기 데이터 vs 연간 데이터**: 교차 검증에는 연간 데이터를 우선 사용, 분기 데이터는 일부 출처가 지연될 수 있음
3. **원본 재무제표 우선**: 두 출처가 모두 원본 재무제표（10-K/연차보고서 PDF）와 불일치하면 원본 재무제표를 기준으로 하고 출처 오류를 표기

---

## 빠른 색인

| 상황 | 주요 출처 | 보조 출처 |
|------|---------|---------|
| PDD / 핀둬둬 | macrotrends.net/stocks/charts/PDD | stockanalysis.com/stocks/pdd |
| 텐센트 | macrotrends.net/stocks/charts/TCEHY | aastocks（0700.HK） |
| 넷이즈 | macrotrends.net/stocks/charts/NTES | aastocks（9999.HK） |
| 37인터랙티브엔터테인먼트 | eastmoney.com（002555） | cninfo.com.cn |
| 지비트 | eastmoney.com（603444） | cninfo.com.cn |
| Nintendo | macrotrends.net/stocks/charts/NTDOY | stockanalysis.com/stocks/ntdoy |
| Capcom | macrotrends（CCOEY） | stockanalysis（CCOEY） |
| 삼성전자 | `py tools/krx_data.py financials 005930` | 네이버 금융 005930 / DART |
| SK하이닉스 | `py tools/krx_data.py financials 000660` | 네이버 금융 000660 / DART |
| 카카오 | `py tools/krx_data.py financials 035720` | 네이버 금융 035720 / DART |
| 쿠팡(美상장) | macrotrends.net/stocks/charts/CPNG | stockanalysis.com/stocks/cpng |
