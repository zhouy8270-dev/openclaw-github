#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import urllib.parse
import sys

sys.setrecursionlimit(10000)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
}

def test_connect():
    url = "https://cn.bing.com"
    print(f"Testing connection to {url}")
    
    try:
        # Longer timeout
        resp = requests.get(url, headers=HEADERS, timeout=30)
        print(f"Connected OK! Status: {resp.status_code}")
        print(f"Page length: {len(resp.text)}")
        return True
    except Exception as e:
        print(f"Connection failed: {type(e).__name__}: {e}")
        return False

if __name__ == "__main__":
    test_connect()
