#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""台客秋 — 把 deals-sync 的 Python 資料庫轉成 Astro 用的 promos.json"""
import json
import os
import sys
import datetime

sys.path.insert(0, os.path.expanduser("~/workspace/deals-sync"))
from deals_data import DELIVERY, SITE
from deals_taxi import TAXI
from deals_travel import TRAVEL, HOME_TOP5, FOOTER_TEXT

SEO = {
    "delivery": {
        "slug": "delivery",
        "seoTitle": "外送優惠碼整理｜Uber Eats、foodpanda 優惠碼 - 台客秋",
        "seoDesc": "2026 最新外送優惠碼整理：Uber Eats 優惠碼、foodpanda 優惠碼、foodomo 優惠，免運、買一送一、地區限定碼每月更新。",
        "h1": "外送優惠碼整理",
        "intro_seo": "肚子餓免忍！台客秋幫你整理 Uber Eats 優惠碼、foodpanda 優惠碼、foodomo 優惠碼，含外送免運、買一送一、店家滿額折扣與地區限定碼，每月更新。優惠碼點了直接連官方 App 使用。",
    },
    "taxi": {
        "slug": "taxi",
        "seoTitle": "叫車優惠碼整理｜Uber、LINE GO、55688 搭車金 - 台客秋",
        "seoDesc": "2026 最新叫車優惠整理：Uber 優惠碼、LINE GO 乘車券、55688 台灣大車隊搭車金、yoxi、Bolt 折扣碼，新戶首搭、機場接送一次看。",
        "h1": "叫車優惠碼整理",
        "intro_seo": "出門免煩惱！台客秋整理 Uber 優惠碼、LINE GO 乘車券、55688 台灣大車隊搭車金、yoxi 優惠碼、Bolt 折扣碼，新戶首搭優惠、機場接送、信用卡綁卡回饋一次整理，上車就省錢。",
    },
    "travel": {
        "slug": "travel",
        "seoTitle": "旅遊優惠碼整理｜KKday、Klook、Agoda 訂房優惠 - 台客秋",
        "seoDesc": "2026 最新旅遊優惠碼：KKday 優惠碼、Klook 優惠碼、Trip.com 折扣碼、Agoda 訂房優惠、Expedia 信用卡碼、Booking.com 會員價，門票住宿機票一次搞定。",
        "h1": "旅遊優惠碼整理",
        "intro_seo": "作夥走跳，玩得比人便宜！台客秋整理 KKday 優惠碼、Klook 優惠碼、Trip.com 折扣碼、Agoda 訂房優惠、Expedia 信用卡優惠碼、Booking.com 會員價，門票、住宿、機票一次搞定，每月更新。",
    },
}

HOME_SEO = {
    "seoTitle": "台客秋｜外送、叫車、旅遊優惠碼整理",
    "seoDesc": "台客秋是每月更新的優惠碼整理小站：Uber Eats 優惠碼、foodpanda 優惠碼、叫車搭車金、KKday／Klook 優惠碼、Agoda 訂房優惠都在這，點了就有省。",
    "h1": "台客秋",
}


def count_deals(page):
    return sum(len(s["deals"]) for pf in page["platforms"] for s in pf["sections"])


AUTO_PATH = os.path.expanduser("~/workspace/deals-sync/auto_deals.json")


def load_auto():
    if not os.path.exists(AUTO_PATH):
        return {}
    with open(AUTO_PATH, encoding="utf-8") as f:
        return json.load(f)


def merge_auto(page, key, auto):
    """把 auto_deals.json 的自動抓取優惠併入各平台，獨立「自動更新」區塊"""
    plat_map = auto.get(key, {})
    if not plat_map:
        return
    for pf in page["platforms"]:
        deals = plat_map.get(pf["name"])
        if not deals:
            continue
        pf["sections"].append({"title": "自動更新", "deals": deals})


def main():
    out = {
        "site": {"name": SITE["name"], "source_name": SITE["source_name"]},
        "updated": datetime.date.today().isoformat(),
        "top5": HOME_TOP5,
        "footer": FOOTER_TEXT,
        "categories": [],
    }
    total = 0
    auto = load_auto()
    for key, page in (("delivery", DELIVERY), ("taxi", TAXI), ("travel", TRAVEL)):
        merge_auto(page, key, auto)
        n = count_deals(page)
        total += n
        out["categories"].append({
            "key": key,
            "slug": SEO[key]["slug"],
            "title": page["title"],
            "intro": page.get("intro", ""),
            "dealCount": n,
            "seo": SEO[key],
            "platforms": page["platforms"],
        })
    out["total"] = total
    out["homeSeo"] = HOME_SEO

    dest = os.path.expanduser("~/workspace/taikeqiu/src/data/promos.json")
    with open(dest, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("wrote", dest, "total deals =", total)


if __name__ == "__main__":
    main()
