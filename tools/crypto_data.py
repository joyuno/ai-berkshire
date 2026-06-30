#!/usr/bin/env python3
"""암호화폐 데이터 도구 — CoinGecko 무료 API, 무외부의존(stdlib only).

Claude Code Skills(/crypto-research)에 메인 코인(BTC/ETH 등)의 시세·시총·공급·도미넌스
데이터를 제공한다. 가격/시총/공급은 CoinGecko에서 정량 취득해 LLM 암산을 배제한다.
설계 원칙: 독립 모듈, urllib 사용(크로스플랫폼), 한국어 출력.

※ 한계: 가격/시총/공급/도미넌스만 제공한다. 활성주소·해시레이트·MVRV·소각량 등
   심층 온체인 지표는 별도 소스(Glassnode/Etherscan/Ultrasound.money 등)를 WebSearch로 보완한다.
   기술적 분석(매매 시그널)은 제공하지 않는다.

사용법(Skill이 자동 호출):
    python3 tools/crypto_data.py quote btc          # 시세·시총·ATH 대비·공급
    python3 tools/crypto_data.py quote ethereum     # 심볼 또는 CoinGecko id 모두 가능
    python3 tools/crypto_data.py global             # 전체 시총·BTC/ETH 도미넌스

Python >= 3.8, 무외부의존.
"""

import argparse
import json
import sys
from urllib.parse import urlencode
from urllib.request import Request, urlopen

try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass

_TIMEOUT = 20
_UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
_BASE = "https://api.coingecko.com/api/v3"

# 메인 코인 심볼 → CoinGecko id (알트는 의도적으로 최소만 매핑)
_SYMBOL_MAP = {
    "btc": "bitcoin", "xbt": "bitcoin", "bitcoin": "bitcoin",
    "eth": "ethereum", "ethereum": "ethereum",
}


def _get_json(path, params=None):
    url = f"{_BASE}{path}"
    if params:
        url = f"{url}?{urlencode(params)}"
    req = Request(url, headers={"User-Agent": _UA})
    with urlopen(req, timeout=_TIMEOUT) as resp:
        return json.loads(resp.read().decode("utf-8"))


def _resolve(coin: str) -> str:
    c = coin.strip().lower()
    return _SYMBOL_MAP.get(c, c)  # 매핑에 없으면 입력을 그대로 id로 사용


def _fmt_usd(v) -> str:
    try:
        v = float(v)
    except (ValueError, TypeError):
        return "-"
    if abs(v) >= 1e12:
        return f"${v/1e12:.2f}T"
    if abs(v) >= 1e9:
        return f"${v/1e9:.2f}B"
    if abs(v) >= 1e6:
        return f"${v/1e6:.2f}M"
    return f"${v:,.2f}"


def cmd_quote(coin: str):
    cid = _resolve(coin)
    try:
        data = _get_json("/coins/markets", {
            "vs_currency": "usd", "ids": cid,
            "price_change_percentage": "24h,30d,1y",
        })
    except Exception as e:
        print(f"❌ {coin} 조회 실패: {e}")
        print("   WebSearch(CoinGecko/CoinMarketCap)로 보완하세요")
        return
    if not data:
        print(f"❌ '{coin}'(id={cid}) 코인을 찾지 못했습니다. CoinGecko id를 확인하세요")
        return
    d = data[0]

    circ = d.get("circulating_supply")
    maxs = d.get("max_supply")
    pct_mined = f"{circ/maxs*100:.1f}%" if (circ and maxs) else "-"

    print("=" * 60)
    print(f"{d.get('name')} ({d.get('symbol','').upper()})  시총순위 #{d.get('market_cap_rank','-')}")
    print("=" * 60)
    print(f"  현재가:        {_fmt_usd(d.get('current_price'))}")
    print(f"  시가총액:      {_fmt_usd(d.get('market_cap'))}")
    print(f"  24h 거래대금:  {_fmt_usd(d.get('total_volume'))}")
    print(f"  24h 변동:      {d.get('price_change_percentage_24h_in_currency', d.get('price_change_percentage_24h')):.2f}%")
    pc30 = d.get("price_change_percentage_30d_in_currency")
    pc1y = d.get("price_change_percentage_1y_in_currency")
    print(f"  30d 변동:      {pc30:.2f}%" if pc30 is not None else "  30d 변동:      -")
    print(f"  1y 변동:       {pc1y:.2f}%" if pc1y is not None else "  1y 변동:       -")
    print(f"  사상최고(ATH): {_fmt_usd(d.get('ath'))} ({str(d.get('ath_date',''))[:10]})")
    print(f"  ATH 대비:      {d.get('ath_change_percentage'):.2f}%" if d.get('ath_change_percentage') is not None else "  ATH 대비:      -")
    print(f"  유통공급:      {circ:,.0f}" if circ else "  유통공급:      -")
    print(f"  최대공급:      {maxs:,.0f}" if maxs else "  최대공급:      무제한/미설정")
    print(f"  채굴/발행률:   {pct_mined}")
    print(f"  완전희석시총:  {_fmt_usd(d.get('fully_diluted_valuation'))}")


def cmd_global():
    try:
        g = _get_json("/global").get("data", {})
    except Exception as e:
        print(f"❌ 글로벌 데이터 조회 실패: {e}")
        return
    mcap = g.get("total_market_cap", {}).get("usd")
    vol = g.get("total_volume", {}).get("usd")
    dom = g.get("market_cap_percentage", {})

    print("=" * 60)
    print("암호화폐 시장 전체 (Global)")
    print("=" * 60)
    print(f"  전체 시가총액:   {_fmt_usd(mcap)}")
    print(f"  24h 거래대금:    {_fmt_usd(vol)}")
    print(f"  활성 코인 수:    {g.get('active_cryptocurrencies','-')}")
    print(f"  BTC 도미넌스:    {dom.get('btc', 0):.1f}%")
    print(f"  ETH 도미넌스:    {dom.get('eth', 0):.1f}%")
    mcap_chg = g.get("market_cap_change_percentage_24h_usd")
    print(f"  시총 24h 변동:   {mcap_chg:.2f}%" if mcap_chg is not None else "  시총 24h 변동:   -")


def main():
    parser = argparse.ArgumentParser(
        description="암호화폐 데이터 도구 — CoinGecko API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = parser.add_subparsers(dest="command")

    p_q = sub.add_parser("quote", help="시세·시총·ATH·공급")
    p_q.add_argument("coin", help="심볼(btc/eth) 또는 CoinGecko id")

    sub.add_parser("global", help="전체 시장·도미넌스")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    if args.command == "quote":
        cmd_quote(args.coin)
    elif args.command == "global":
        cmd_global()


if __name__ == "__main__":
    main()
