import requests
import feedparser
import re
from datetime import datetime
import xml.etree.ElementTree as ET

def strip_html(text):
    """Universal function to remove all HTML tags."""
    if not text: return ""
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text).strip()

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
            
            clean_text = strip_html(entry.get('summary', ''))
            return {"title": "The Verge", "text": f"{entry.title}: {clean_text[:150]}..."}
    except Exception as e:
        print(f"Verge RSS Error: {e}")
    return {"title": "The Verge", "text": "Tech news currently unavailable."}

def fetch_history_module():
    url = "https://history.muffinlabs.com/date"
    try:
        events = requests.get(url, timeout=5).json()['data']['Events']
        
        selected_events = [{"year": e['year'], "text": strip_html(e['text'])} for e in events if len(e['text']) < 150][:2]
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
            for entry in feed.entries[:1]:
                clean_text = strip_html(entry.get('summary', ''))
                items.append({"title": entry.title, "summary": f"{clean_text[:200]}..."})
            return items
    except Exception as e:
        print(f"Sports RSS Error: {e}")
    return [{"title": "Scores unavailable.", "summary": ""}]

def fetch_good_news_module():
    """Fetches good news and strips out all HTML and URLs."""
    try:
        url = "https://www.goodnewsnetwork.org/feed/"
        headers = {"User-Agent": "TheDailyInk/1.0"}
        response = requests.get(url, headers=headers, timeout=5)
        
        root = ET.fromstring(response.content)
        item = root.find('.//item')
        title = strip_html(item.find('title').text)
        summary = strip_html(item.find('description').text)
        
        
        summary = summary.replace("[&hellip;]", "...").strip()
        
        return {"title": title, "text": summary}
        
    except Exception as e:
        print(f"Good News Network Error: {e}")
        return {"title": "Daily Positivity", "text": "Everything is going to be okay today."}
    
def fetch_curated_news_module():
    """Fetches global news and filters for uplifting or positive emotion tags."""
    url = "https://actually-relevant-api.onrender.com/api/stories"
    
    
    positive_tags = ["uplifting", "hopeful", "inspiring", "happy", "optimistic", "good"]
    
    try:
        response = requests.get(url, timeout=45)
        response.raise_for_status() 
        data = response.json()
        
        stories = []
        if isinstance(data, list):
            stories = data
        elif isinstance(data, dict):
            stories = data.get("stories") or data.get("data") or []
            
        if stories:
            
            for story in stories:
                emotion = story.get("emotionTag", "").lower()
                
                if emotion in positive_tags:
                    title = story.get("title", "Uplifting News")
                    text_content = story.get("summary") or story.get("relevanceSummary") or "No details available."
                    
                    clean_text = strip_html(str(text_content)).strip()
                    truncated_text = clean_text[:900] + "..." if len(clean_text) > 900 else clean_text
                    
                    return {
                        "title": title,
                        "text": truncated_text
                    }
            
            
            return {
                "title": "Uplifting News", 
                "text": "No highly-rated uplifting stories in the global feed right now, but good things are still happening everywhere."
            }
            
    except requests.exceptions.Timeout:
        print("Uplifting News API Error: Timeout.")
    except Exception as e:
        print(f"Uplifting News API Error: {type(e).__name__} - {e}")
        
    return {"title": "Uplifting News", "text": "World news feed temporarily unavailable."}

