#!/usr/bin/env python3
"""한국 주식 데이터 도구 — 네이버 금융 API, 무외부의존(stdlib only).

Claude Code Skills에 한국(KOSPI/KOSDAQ) 실시간 시세·재무·밸류에이션 데이터를 제공한다.
설계 원칙: 독립 모듈, 기존 도구에 영향 없음. urllib 사용(크로스플랫폼, curl 불필요).
A주는 tools/ashare_data.py, 한국은 이 도구를 사용한다.

사용법(Skill이 자동 호출, 수동 실행 불필요):
    python3 tools/krx_data.py quote 005930        # 실시간 시세 (삼성전자)
    python3 tools/krx_data.py financials 005930    # 핵심 재무 (최근 4년, 단위 억원)
    python3 tools/krx_data.py valuation 005930     # 밸류에이션 지표
    python3 tools/krx_data.py search 삼성전자       # 종목코드 검색

Python >= 3.8, 무외부의존.
"""

import argparse
import json
import sys
from urllib.parse import quote as urlquote
from urllib.request import Request, urlopen

# Windows 콘솔(cp949)에서도 한글이 깨지지 않도록 UTF-8 출력 강제
try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass

_TIMEOUT = 15
_UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
_BASE = "https://m.stock.naver.com/api/stock"


def _get_json(url):
    """네이버 금융 API에서 JSON 취득."""
    req = Request(url, headers={"User-Agent": _UA})
    with urlopen(req, timeout=_TIMEOUT) as resp:
        return json.loads(resp.read().decode("utf-8"))


def _totalinfo_dict(integration: dict) -> dict:
    """integration.totalInfos 리스트를 code→value 딕셔너리로 변환."""
    out = {}
    for item in integration.get("totalInfos", []):
        out[item.get("code")] = item.get("value", "-")
    return out


# ---------------------------------------------------------------------------
# 명령 구현
# ---------------------------------------------------------------------------

def cmd_quote(code: str):
    """실시간 시세 스냅샷."""
    try:
        basic = _get_json(f"{_BASE}/{code}/basic")
        integ = _get_json(f"{_BASE}/{code}/integration")
    except Exception as e:
        print(f"❌ 종목 {code} 조회 실패: {e}")
        print("   WebSearch(네이버 금융 / DART)로 보완하세요")
        return

    name = basic.get("stockName", code)
    market = basic.get("stockExchangeName", "-")
    ti = _totalinfo_dict(integ)

    print("=" * 60)
    print(f"실시간 시세: {name} ({code}) [{market}]")
    print("=" * 60)
    print(f"  현재가:       {basic.get('closePrice', '-')} 원")
    print(f"  등락률:       {basic.get('fluctuationsRatio', '-')}%")
    print(f"  전일대비:     {basic.get('compareToPreviousClosePrice', '-')}")
    print(f"  전일종가:     {ti.get('lastClosePrice', '-')}")
    print(f"  시가:         {ti.get('openPrice', '-')}")
    print(f"  고가:         {ti.get('highPrice', '-')}")
    print(f"  저가:         {ti.get('lowPrice', '-')}")
    print(f"  거래량:       {ti.get('accumulatedTradingVolume', '-')}")
    print(f"  거래대금:     {ti.get('accumulatedTradingValue', '-')}")
    print(f"  시가총액:     {ti.get('marketValue', '-')}")
    print(f"  외인소진율:   {ti.get('foreignRate', '-')}")
    print(f"  PER:          {ti.get('per', '-')}")
    print(f"  PBR:          {ti.get('pbr', '-')}")
    print(f"  EPS:          {ti.get('eps', '-')}")
    print(f"  BPS:          {ti.get('bps', '-')}")
    print(f"  52주 최고:    {ti.get('highPriceOf52Weeks', '-')}")
    print(f"  52주 최저:    {ti.get('lowPriceOf52Weeks', '-')}")


def cmd_valuation(code: str):
    """밸류에이션 지표 모음."""
    try:
        basic = _get_json(f"{_BASE}/{code}/basic")
        integ = _get_json(f"{_BASE}/{code}/integration")
    except Exception as e:
        print(f"❌ 종목 {code} 조회 실패: {e}")
        print("   WebSearch(네이버 금융 / DART)로 보완하세요")
        return

    name = basic.get("stockName", code)
    market = basic.get("stockExchangeName", "-")
    ti = _totalinfo_dict(integ)

    print("=" * 60)
    print(f"밸류에이션 지표: {name} ({code}) [{market}]")
    print("=" * 60)
    print(f"  현재가:       {basic.get('closePrice', '-')} 원")
    print(f"  시가총액:     {ti.get('marketValue', '-')}")
    print(f"  PER:          {ti.get('per', '-')}")
    print(f"  추정PER:      {ti.get('cnsPer', '-')}")
    print(f"  PBR:          {ti.get('pbr', '-')}")
    print(f"  EPS:          {ti.get('eps', '-')}")
    print(f"  추정EPS:      {ti.get('cnsEps', '-')}")
    print(f"  BPS:          {ti.get('bps', '-')}")
    print(f"  배당수익률:   {ti.get('dividendYieldRatio', '-')}")
    print(f"  주당배당금:   {ti.get('dividend', '-')}")
    print(f"  52주 최고:    {ti.get('highPriceOf52Weeks', '-')}")
    print(f"  52주 최저:    {ti.get('lowPriceOf52Weeks', '-')}")


# 재무제표에서 출력할 항목(있는 것만 출력)
_FIN_ROWS = [
    "매출액", "영업이익", "당기순이익", "지배주주순이익",
    "영업이익률", "순이익률", "ROE", "ROA", "부채비율",
    "EPS", "PER", "BPS", "PBR", "주당배당금", "시가배당률",
]


def cmd_financials(code: str):
    """최근 연도별 핵심 재무 데이터 (금액 단위: 억원)."""
    try:
        data = _get_json(f"{_BASE}/{code}/finance/annual")
    except Exception as e:
        print(f"❌ 종목 {code} 재무 조회 실패: {e}")
        print("   WebSearch(네이버 금융 / DART)로 보완하세요")
        return

    fin = data.get("financeInfo", {})
    titles = fin.get("trTitleList", [])
    rows = fin.get("rowList", [])

    if not titles or not rows:
        print(f"⚠️ {code} 재무 데이터를 가져오지 못했습니다. WebSearch로 보완하세요")
        return

    # 기간 컬럼 순서(key) + 라벨, 컨센서스 여부
    periods = [(t["key"], t["title"], t.get("isConsensus") == "Y") for t in titles]

    # title→{key:value}
    row_map = {}
    for r in rows:
        cols = {k: v.get("value", "-") for k, v in r.get("columns", {}).items()}
        row_map[r.get("title", "")] = cols

    print("=" * 60)
    print(f"핵심 재무 데이터: {code}  (금액 단위: 억원, E=컨센서스 추정)")
    print("=" * 60)

    header = "  " + " ".ljust(14)
    for key, label, est in periods:
        tag = label.rstrip(".") + ("E" if est else "")
        header += tag.rjust(13)
    print(header)
    print("  " + "-" * (14 + 13 * len(periods)))

    for name in _FIN_ROWS:
        if name not in row_map:
            continue
        line = "  " + name.ljust(14)
        for key, _label, _est in periods:
            line += str(row_map[name].get(key, "-")).rjust(13)
        print(line)


def cmd_search(keyword: str):
    """종목코드 검색."""
    url = f"https://ac.stock.naver.com/ac?q={urlquote(keyword)}&target=stock"
    try:
        data = _get_json(url)
    except Exception as e:
        print(f"❌ '{keyword}' 검색 실패: {e}")
        return

    items = data.get("items", [])
    if not items:
        print(f"❌ '{keyword}' 와 일치하는 종목을 찾지 못했습니다")
        return

    print("=" * 60)
    print(f"검색 결과: '{keyword}'")
    print("=" * 60)
    for it in items:
        code = it.get("code", "")
        name = it.get("name", "")
        mkt = it.get("typeName", "")
        nation = it.get("nationName", "")
        print(f"  {code}  {name}  [{mkt}/{nation}]")


# ---------------------------------------------------------------------------
# CLI 진입점
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="한국 주식 데이터 도구 — 네이버 금융 API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = parser.add_subparsers(dest="command")

    p_quote = sub.add_parser("quote", help="실시간 시세")
    p_quote.add_argument("code", help="종목코드, 예) 005930")

    p_fin = sub.add_parser("financials", help="핵심 재무 데이터(연도별)")
    p_fin.add_argument("code", help="종목코드")

    p_val = sub.add_parser("valuation", help="밸류에이션 지표")
    p_val.add_argument("code", help="종목코드")

    p_search = sub.add_parser("search", help="종목코드 검색")
    p_search.add_argument("keyword", help="회사명 또는 키워드")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    cmds = {
        "quote": lambda: cmd_quote(args.code),
        "financials": lambda: cmd_financials(args.code),
        "valuation": lambda: cmd_valuation(args.code),
        "search": lambda: cmd_search(args.keyword),
    }
    cmds[args.command]()


if __name__ == "__main__":
    main()
