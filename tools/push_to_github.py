#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""台客秋 — 推送網站原始碼到 GitHub（taipeiwolf2/taikeqiu）。

透過 ~/workspace/skills/github/bin/gh_api.py 呼叫 GitHub API，
認證走 custom.github connector，不經手 token 明文。

用法：python3 tools/push_to_github.py [commit-message]
"""
import os
import subprocess
import sys

GH_API = os.path.expanduser("~/workspace/skills/github/bin/gh_api.py")
OWNER = "taipeiwolf2"
REPO = "taikeqiu"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

FILES = [
    "package.json",
    "astro.config.mjs",
    "tsconfig.json",
    ".gitignore",
    "README.md",
    "src/data/promos.json",
    "src/layouts/Layout.astro",
    "src/components/DealCard.astro",
    "src/pages/index.astro",
    "src/pages/[category].astro",
    "src/pages/slash.astro",
    "src/pages/about.astro",
    "public/robots.txt",
    "public/llms.txt",
    "public/favicon.svg",
    "public/img/slash-uber.jpg",
    "public/img/slash-panda.jpg",
    "public/img/slash-lala.jpg",
    "public/img/hero-mascot.jpg",
    "public/img/cat-delivery.jpg",
    "public/img/cat-taxi.jpg",
    "public/img/cat-travel.jpg",
    "tools/build_promos.py",
    "tools/push_to_github.py",
]


def main():
    msg = sys.argv[1] if len(sys.argv) > 1 else "更新網站"
    ok = True
    for rel in FILES:
        local = os.path.join(ROOT, rel)
        if not os.path.exists(local):
            print("跳過（無此檔）：%s" % rel)
            continue
        # 檔名括號需 URL 編碼
        repo_path = rel.replace("[", "%5B").replace("]", "%5D")
        r = subprocess.run(
            [GH_API, "--put-file", local, "--repo-path", repo_path,
             "--message", "%s：%s" % (msg, rel),
             "--owner", OWNER, "--repo", REPO],
            capture_output=True, text=True, timeout=120)
        status = (r.stdout.split("\n", 1)[0] or "?").strip()
        print("%s  %s" % (status, rel))
        if not status.startswith("20"):
            ok = False
    print("完成：https://github.com/%s/%s" % (OWNER, REPO) if ok else "部分失敗，請檢查上方狀態碼")


if __name__ == "__main__":
    main()
