#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import urllib.parse
from datetime import datetime

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
}

def search_baidu_news(keyword):
    url = f"https://news.baidu.com/ns?word={urllib.parse.quote(keyword)}&pn=0&cl=2&ct=1&tn=news&rn=10"
    print(f"Searching: {keyword} -> {url}")
    
    try:
        resp = requests.get(url, headers=HEADERS, timeout=20)
        resp.encoding = 'utf-8'
        print(f"Status: {resp.status_code}, Length: {len(resp.text)}")
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        
        results = []
        items = soup.select(".result")
        print(f"Found {len(items)} items in HTML")
        
        for item in items:
            title_tag = item.select_one("h3 a")
            if not title_tag:
                continue
            
            title = title_tag.get_text(strip=True)
            if not title or len(title) < 10:
                continue
                
            link = title_tag.get("href") if title_tag.has_attr("href") else None
            if not link:
                continue
            
            summary_tag = item.select_one(".c-summary")
            summary = ""
            if summary_tag:
                for extra in summary_tag.select(".c-author, .c-info, em"):
                    extra.decompose()
                summary = summary_tag.get_text(strip=True)
            
            results.append({
                "title": title,
                "url": link,
                "summary": summary
            })
        
        print(f"\nGot {len(results)} valid results:")
        for i, r in enumerate(results):
            print(f"\n{i+1}. {r['title']}")
            if r['summary']:
                print(f"   {r['summary'][:80]}")
        
        return results
        
    except Exception as e:
        print(f"Error: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return []

if __name__ == "__main__":
    search_baidu_news("科技新闻 最新")
