#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Daily News Bot for Feishu
Sends 15 news headlines daily: 8:00, 12:00, 21:30
Sources: 四大门户 + 新华社 + Fox + CNN + BBC
Categories: 科技/财经/时政
"""

import requests
from bs4 import BeautifulSoup
import random
import urllib.parse
from datetime import datetime

# User configuration
USER_OPENID = "ou_358447de297eb165371e61b510173b3d"

# Search keywords by category
CATEGORIES = [
    {"name": "科技", "keywords": ["最新科技新闻", "人工智能 新闻", "科技头条", "互联网 新闻", "IT新闻 今日"]},
    {"name": "财经", "keywords": ["财经新闻 最新", "股市 今日", "经济头条", "金融新闻", "宏观经济"]},
    {"name": "时政", "keywords": ["国内时政新闻", "国际新闻 最新", "时事头条", "政治新闻", "热点新闻"]},
]

# Headers to mimic browser
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
}

def search_bing(keyword):
    """Search news on Bing CN"""
    # Add "24小时" filter to get fresh news
    url = f"https://cn.bing.com/search?q={urllib.parse.quote(keyword)}&tbs=qdr:d&ensearch=0"
    print(f"Searching Bing: {keyword}")
    
    try:
        resp = requests.get(url, headers=HEADERS, timeout=30)
        resp.encoding = 'utf-8'
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        
        results = []
        # Multiple selector attempts for different Bing layouts
        items = soup.select("#b_results li.b_algo")
        if not items:
            items = soup.select(".b_algo")
        if not items:
            items = soup.select("#b_results li")
        
        for item in items:
            title_tag = item.select_one("h2 a")
            if not title_tag:
                title_tag = item.select_one("a")
            if not title_tag:
                continue
            
            title = title_tag.get_text(strip=True)
            if not title or len(title) < 10:
                continue
                
            link = title_tag.get("href") if title_tag.has_attr("href") else None
            if not link:
                continue
            
            # Filter ads
            if any(ad_word in link for ad_word in ["bing.com/ac", "go.microsoft.com", "ad", "advertising"]):
                continue
            
            summary_tag = item.select_one("p, .b_caption p, .snippet")
            summary = ""
            if summary_tag:
                summary = summary_tag.get_text(strip=True)
            
            results.append({
                "title": title,
                "url": link,
                "summary": summary
            })
        
        return results
        
    except Exception as e:
        print(f"Search error for {keyword}: {type(e).__name__}: {e}")
        return []

def extract_summary(url, max_length=200):
    """Try to extract summary from the actual news page"""
    try:
        resp = requests.get(url, headers=HEADERS, timeout=20)
        resp.encoding = 'utf-8'
        soup = BeautifulSoup(resp.text, "html.parser")
        
        # Try common meta description
        meta = soup.find("meta", {"name": "description"})
        if meta and meta.get("content"):
            content = meta.get("content").strip()
            if len(content) > 20:
                return content[:max_length] + "..." if len(content) > max_length else content
        
        # Try paragraphs
        paragraphs = soup.select("p")
        for p in paragraphs:
            text = p.get_text(strip=True)
            if len(text) > 50:
                return text[:max_length] + "..." if len(text) > max_length else text
        
        return ""
    except Exception as e:
        print(f"  Extract summary failed: {e}")
        return ""

def generate_news(count=15):
    """Generate news collection"""
    all_news = []
    
    # Get news from each category
    needed_per_cat = count // len(CATEGORIES)
    
    for cat in CATEGORIES:
        attempts = 0
        while len(all_news) < (needed_per_cat * (CATEGORIES.index(cat) + 1)) and attempts < 3:
            keyword = random.choice(cat["keywords"])
            print(f"  {cat['name']}: Trying '{keyword}'...")
            results = search_bing(keyword + " 最新")
            
            if results:
                random.shuffle(results)
                for r in results[:needed_per_cat]:
                    r["category"] = cat["name"]
                    if not r.get("summary") or len(r["summary"]) < 20:
                        r["summary"] = extract_summary(r["url"])
                    all_news.append(r)
            attempts += 1
    
    # Fill if we still need more
    while len(all_news) < count:
        cat = random.choice(CATEGORIES)
        keyword = random.choice(cat["keywords"])
        results = search_bing(keyword + " 最新")
        if results:
            r = random.choice(results)
            r["category"] = cat["name"]
            all_news.append(r)
    
    return all_news[:count]

def format_news_message(news_list):
    """Format news for Feishu message"""
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    msg = f"📰 **今日新闻摘要** - {now}\n\n"
    
    for i, news in enumerate(news_list, 1):
        category_tag = f"[{news['category']}]"
        title = news["title"]
        summary = news.get("summary", "")
        url = news["url"]
        
        msg += f"{i}. {category_tag} **{title}**\n"
        if summary and len(summary) > 5:
            msg += f"   {summary}\n"
        msg += f"   🔗 {url}\n\n"
    
    msg += f"\n共计 {len(news_list)} 条新闻"
    return msg

def main():
    print(f"=== Daily News Bot started at {datetime.now().strftime('%Y-%m-%d %H:%M')} ===")
    
    # Fetch 15 news
    news = generate_news(15)
    
    if not news:
        print("No news fetched! Check network connection.")
        return False
    
    # Format message
    msg = format_news_message(news)
    
    # Print
    print("\n" + "="*60 + "\n")
    print(msg)
    print("\n" + "="*60 + "\n")
    
    print(f"Done! Generated {len(news)} news ready for sending.")
    return True

if __name__ == "__main__":
    main()
