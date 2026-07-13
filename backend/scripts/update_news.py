#!/usr/bin/env python3
import os, sys, json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from app import fetch_news_from_api, save_cached_news, fallback_news

if __name__ == '__main__':
    try:
        articles = fetch_news_from_api()
        if articles:
            save_cached_news(articles)
            print(f'Saved {len(articles)} articles to cache')
        else:
            raise RuntimeError('No articles returned')
    except Exception as e:
        print('News fetch failed:', e)
        fallback = fallback_news()
        save_cached_news(fallback)
        print(f'Wrote fallback news cache with {len(fallback)} items')
