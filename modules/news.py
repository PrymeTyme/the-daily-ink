import requests
import feedparser
import re
from datetime import datetime

def fetch_wiki_module():
    date_str = datetime.now().strftime("%Y/%m/%d")
    url = f"https://en.wikipedia.org/api/rest_v1/feed/featured/{date_str}"
    headers = {"User-Agent": "TheDailyInk/1.0"}
    try:
        response = requests.get(url, headers=headers, timeout=5)
        data = response.json()
        tfa = data.get("tfa", {})
        extract = tfa.get("extract", "No summary.")
        return {
            "title": tfa.get("normalizedtitle", "Daily Wiki"),
            "text": extract[:950] + "..." if len(extract) > 950 else extract,
        }
    except Exception as e:
        print(f"Wiki API Error: {e}")
        return {"title": "Daily Wiki", "text": "Content unavailable."}

def fetch_verge_module():
    url = "https://www.theverge.com/rss/index.xml"
    try:
        feed = feedparser.parse(url)
        if feed.entries:
            entry = feed.entries[0]
            clean_text = re.sub('<[^<]+?>', '', entry.get('summary', ''))
            return {"title": "The Verge", "text": f"{entry.title}: {clean_text[:150]}..."}
    except Exception as e:
        print(f"Verge RSS Error: {e}")
    return {"title": "The Verge", "text": "Tech news currently unavailable."}

def fetch_history_module():
    url = "https://history.muffinlabs.com/date"
    try:
        events = requests.get(url, timeout=5).json()['data']['Events']
        selected_events = [{"year": e['year'], "text": e['text']} for e in events if len(e['text']) < 150][:2]
        return {"title": "On This Day", "items": selected_events}
    except Exception as e:
        print(f"History API Error: {e}")
        return {"title": "On This Day", "items": []}

def fetch_sports_module():
    url = "https://www.espn.com/espn/rss/news"
    try:
        feed = feedparser.parse(url)
        if feed.entries:
            items = []
            # FIX: Changed from [:2] to [:1] to only grab the single top headline
            for entry in feed.entries[:1]:
                clean_text = re.sub('<[^<]+?>', '', entry.get('summary', ''))
                # FIX: Shortened the summary from 90 characters down to 60
                items.append({"title": entry.title, "summary": f"{clean_text[:60]}..."})
            return items
    except Exception as e:
        print(f"Sports RSS Error: {e}")
    return [{"title": "Scores unavailable.", "summary": ""}]