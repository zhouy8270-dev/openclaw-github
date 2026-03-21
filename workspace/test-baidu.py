#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import urllib.parse

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
}

def search_baidu(keyword):
    url = f"https://www.baidu.com/s?wd={urllib.parse.quote(keyword)}"
    print(f"Searching Baidu: {url}")
    
    try:
        resp = requests.get(url, headers=HEADERS, timeout=15)
        print(f"Status: {resp.status_code}")
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        
        results = []
        items = soup.select(".result")
        
        for item in items:
            title_tag = item.select_one("h3 a, .t a")
            if not title_tag:
                continue
            
            title = title_tag.get_text(strip=True)
            if not title or len(title) < 5:
                continue
                
            link = title_tag.get("href") if title_tag.has_attr("href") else None
            if not link:
                continue
            
            # Get real URL from Baidu redirect
            if link.startswith("/"):
                link = "https://www.baidu.com" + link
                
            summary_tag = item.select_one(".c-abstract, .abstract")
            summary = ""
            if summary_tag:
                summary = summary_tag.get_text(strip=True)
            
            results.append({
                "title": title,
                "url": link,
                "summary": summary
            })
        
        print(f"Found {len(results)} results")
        for i, r in enumerate(results[:5]):
            print(f"\n{i+1}. {r['title']}")
            if r['summary']:
                print(f"   {r['summary'][:100]}...")
        
        return results
        
    except Exception as e:
        print(f"Error: {e}")
        return []

if __name__ == "__main__":
    search_baidu("科技新闻 最新")
