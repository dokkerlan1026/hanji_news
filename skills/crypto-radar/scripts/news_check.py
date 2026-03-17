#!/usr/bin/env python3
import argparse
import json
import re
import sys
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

POSITIVE = [
    "listing", "listed", "launch", "partnership", "upgrade", "mainnet", "integration",
    "etf", "funding", "investment", "token burn", "burn", "airdrop", "roadmap"
]
NEGATIVE = [
    "hack", "exploit", "lawsuit", "delist", "delisting", "scam", "rug", "liquidation",
    "sell-off", "dump", "warning", "fraud", "probe", "investigation"
]
HYPE = [
    "soars", "skyrockets", "surges", "moon", "100x", "explodes", "parabolic"
]


def fetch_rss(query):
    url = "https://news.google.com/rss/search?hl=en-US&gl=US&ceid=US:en&q=" + urllib.parse.quote(query)
    with urllib.request.urlopen(url, timeout=20) as r:
        return r.read()


def parse_items(xml_bytes, limit=8):
    root = ET.fromstring(xml_bytes)
    items = []
    for item in root.findall(".//item")[:limit]:
        title = (item.findtext("title") or "").strip()
        link = (item.findtext("link") or "").strip()
        pub = (item.findtext("pubDate") or "").strip()
        items.append({"title": title, "link": link, "pubDate": pub})
    return items


def score_items(items):
    pos = 0
    neg = 0
    hype = 0
    for it in items:
        t = it["title"].lower()
        if any(k in t for k in POSITIVE):
            pos += 1
        if any(k in t for k in NEGATIVE):
            neg += 1
        if any(k in t for k in HYPE):
            hype += 1
    verdict = "neutral"
    if pos > neg and pos >= 1:
        verdict = "supportive"
    if neg > pos and neg >= 1:
        verdict = "risk"
    if hype >= 2 and pos == 0:
        verdict = "hypey"
    return {"positive_hits": pos, "negative_hits": neg, "hype_hits": hype, "verdict": verdict}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("symbol")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    base = args.symbol.upper().replace("USDT", "")
    queries = [
        f'{base} crypto',
        f'{base} token listing partnership upgrade',
        f'Binance {base}'
    ]
    seen = set()
    items = []
    for q in queries:
        try:
            rss = fetch_rss(q)
            for it in parse_items(rss):
                key = (it['title'], it['link'])
                if key in seen:
                    continue
                seen.add(key)
                items.append(it)
        except Exception:
            continue
    items = items[:10]
    result = {"symbol": args.symbol.upper(), "summary": score_items(items), "headlines": items}
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"{result['symbol']} news verdict={result['summary']['verdict']} pos={result['summary']['positive_hits']} neg={result['summary']['negative_hits']} hype={result['summary']['hype_hits']}")
        for h in items[:5]:
            print(f"- {h['title']}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)
