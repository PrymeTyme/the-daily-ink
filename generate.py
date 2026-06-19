import os
import requests
from datetime import datetime
import feedparser
import re
from dotenv import load_dotenv
from PIL import Image
from io import BytesIO
import random
from html2image import Html2Image


load_dotenv()

# --- INITIALISATION ---
#
try:
    edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    if os.path.exists(edge_path):
        hti = Html2Image(browser_executable=edge_path)
    else:
        hti = Html2Image() 
except Exception as e:
    print(f"Error initializing browser: {e}")
    exit(1)

# --- CONTENT MODULES ---

def get_weather():
    api_key = os.getenv("OPENWEATHER_API_KEY")
    
    city = os.getenv("WEATHER_CITY", "Schwarzach, AT") 
    
    if not api_key:
        print("Weather Error: OPENWEATHER_API_KEY is missing!")
        return "Weather N/A"
        
    
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=en"
    
    try:
        response = requests.get(url, timeout=5)
        data = response.json()
        
        if response.status_code != 200:
            print(f"Weather API Error: {data.get('message', 'Unknown Error')}")
            return "Weather N/A"
            
        return f"{round(data['main']['temp'])}°C, {data['weather'][0]['description'].title()}"
    except Exception as e:
        print(f"Weather Network Error: {e}")
        return "Weather N/A"

def fetch_wiki_module():
    date_str = datetime.now().strftime("%Y/%m/%d")
    url = f"https://en.wikipedia.org/api/rest_v1/feed/featured/{date_str}"
    headers = {"User-Agent": "TheDailyInk/1.0"}
    try:
        data = requests.get(url, headers=headers, timeout=5).json()
        tfa = data.get("tfa", {})
        extract = tfa.get("extract", "No summary.")
        return {
            "title": tfa.get("normalizedtitle", "Daily Wiki"),
            "text": extract[:950] + "..." if len(extract) > 950 else extract,
        }
    except:
        return {"title": "Daily Wiki", "text": "Content unavailable."}

def fetch_facts_module():
    url = "https://uselessfacts.jsph.pl/api/v2/facts/random?language=en"
    facts = []
    for _ in range(3):
        try:
            facts.append(requests.get(url, timeout=3).json().get("text", "Fact unavailable."))
        except:
            facts.append("Vintage newspapers relied on telegraphs.")
    return facts

def fetch_verge_module():
    url = "https://www.theverge.com/rss/index.xml"
    try:
        feed = feedparser.parse(url)
        if feed.entries:
            entry = feed.entries[0]
            clean_text = re.sub('<[^<]+?>', '', entry.get('summary', ''))
            return {"title": "The Verge", "text": f"{entry.title}: {clean_text[:250]}..."}
    except:
        pass
    return {"title": "The Verge", "text": "Tech news currently unavailable."}

def fetch_history_module():
    url = "https://history.muffinlabs.com/date"
    try:
        events = requests.get(url, timeout=5).json()['data']['Events']
        selected_events = [{"year": e['year'], "text": e['text']} for e in events if len(e['text']) < 150][:2]
        return {"title": "On This Day", "items": selected_events}
    except:
        return {"title": "On This Day", "items": []}

def fetch_word_module():
    try:
        data = requests.get("https://api.wordnik.com/v4/words.json/wordOfTheDay?api_key=YOUR_API_KEY", timeout=3).json()
        return {"word": data['word'], "def": data['definitions'][0]['text']}
    except:
        return {"word": "Serendipity", "def": "The occurrence of events by chance in a happy or beneficial way."}

def fetch_quote_module():
    try:
        data = requests.get("https://zenquotes.io/api/today", timeout=3).json()[0]
        return f"{data['q']} — {data['a']}"
    except:
        return "Stay curious. — Unknown"

def fetch_fitting_xkcd():
    for _ in range(10):
        try:
            rid = random.randint(1, 2900)
            data = requests.get(f"https://xkcd.com/{rid}/info.0.json", timeout=3).json()
            img = Image.open(BytesIO(requests.get(data['img'], timeout=3).content))
            if 1.5 <= (img.width / img.height) <= 3.0 and img.width <= 750:
                return {"title": data.get("title", "XKCD"), "img_url": data['img']}
        except: continue
    return {"title": "Wisdom", "img_url": "https://imgs.xkcd.com/comics/wisdom_of_the_ancients.png"}

# --- AGGREGATOR ---

def get_newspaper_data():
    return {
        "date": datetime.now().strftime("%A, %B %d, %Y").upper(),
        "weather": get_weather(),
        "wiki": fetch_wiki_module(),
        "facts": fetch_facts_module(),
        "news": fetch_verge_module(),      
        "history": fetch_history_module(), 
        "quote": fetch_quote_module(),
        "comic": fetch_fitting_xkcd(),
        "word": fetch_word_module()
    }

# --- GENERATOR LOGIK ---

def generate_newspaper():
    print("Fetching data and generating HTML...")
    d = get_newspaper_data()
    facts_list = "".join([f"<li>{f}</li>" for f in d['facts']])
    
    html = f"""
    <html>
    <head>
        <link href="https://fonts.googleapis.com/css2?family=Merriweather:wght@700&family=Oswald:wght@700&display=swap" rel="stylesheet">
        <style>
            body {{ font-family: 'Merriweather', serif; margin: 0; padding: 0; width: 480px; height: 800px; background: white; display: flex; justify-content: center; }}
            .newspaper-wrapper {{ width: 450px; padding: 15px 0; box-sizing: border-box; display: flex; flex-direction: column; }}
            .header {{ text-align: center; border-top: 4px solid black; border-bottom: 5px double black; padding: 10px 0; margin-bottom: 15px; }}
            .title {{ font-family: 'Oswald', sans-serif; font-size: 44px; text-transform: uppercase; font-weight: 700; line-height: 1; }}
            .meta {{ font-family: 'Oswald', sans-serif; font-size: 11px; display: flex; justify-content: space-between; border-top: 1px solid black; padding-top: 4px; margin-top: 6px; }}
            .columns {{ display: flex; gap: 0; height: 490px; overflow: hidden; margin-bottom: 10px; }}
            .col-left {{ flex: 1.8; border-right: 2px solid black; display: flex; flex-direction: column; justify-content: space-between; padding-right: 13px; }}
            .col-right {{ flex: 1; padding-left: 15px; }}
            h2 {{ font-family: 'Oswald', sans-serif; font-size: 14px; border-bottom: 2px solid black; text-transform: uppercase; text-align: center; margin: 0 0 10px 0; padding-bottom: 4px; }}
            ul {{ padding-left: 15px; margin: 0; }}
            li {{ margin-bottom: 8px; font-size: 11px; font-weight: 700; font-family: 'Merriweather', serif; }}
            p {{ margin: 0 0 10px 0; font-family: 'Merriweather', serif; }}
            .dropcap:first-letter {{ float: left; font-size: 38px; font-family: 'Oswald', sans-serif; padding-right: 6px; line-height: 0.8; }}
            .comic-wrapper {{ border-top: 5px double black; padding-top: 8px; }}
            .comic-img {{ width: 100%; height: 125px; object-fit: contain; filter: grayscale(100%) contrast(1.2); }}
            .quote {{ font-size: 11px; font-style: italic; text-align: center; margin-bottom: 8px; font-family: 'Merriweather', serif; }}
            .news-block {{ margin-top: 15px; }}
            .news-content {{ font-family: 'Merriweather', serif; font-weight: 700; font-size: 11px; line-height: 1.4; margin: 0; }}
        </style>
    </head>
    <body>
        <div class="newspaper-wrapper">
            <div class="header">
                <div class="title">The Daily Ink</div>
                <div class="meta">
                    <span>VOL. I ... NO. 1</span>
                    <span>{d['date']}</span>
                    <span>{d['weather']}</span>
                </div>
            </div>
            <div class="columns">
                <div class="col-left">
                    <div>
                        <h2>Daily Wiki</h2>
                        <div style="font-weight:700; text-align:center; font-family:'Oswald', sans-serif; margin-bottom:6px;">{d['wiki']['title']}</div>
                        <p class="dropcap" style="font-weight:700; font-size:11.5px;">{d['wiki']['text']}</p>
                    </div>
                    <div class="news-block" style="margin-top: 10px; margin-bottom: 10px;">
                        <h2>{d['history']['title']}</h2>
                        <div class="news-content">
                            {"".join([f'<div style="margin-bottom:8px;"><b>{item["year"]}</b>: {item["text"]}</div>' for item in d['history']['items']])}
                        </div>
                    </div>
                    <div style="margin-top: auto; border-top: 2px solid black; padding-top: 8px;">
                        <div style="font-family:'Oswald', sans-serif; font-size: 13px; font-weight:700; text-transform: uppercase; margin-bottom: 2px;">
                            Word of the Day: {d['word']['word']}
                        </div>
                        <div style="font-size: 11px; font-style: italic; line-height: 1.3;">
                            {d['word']['def']}
                        </div>
                    </div>
                </div>
                <div class="col-right">
                    <h2>Did You Know?</h2>
                    <ul>{facts_list}</ul>
                    <div class="news-block">
                        <h2>{d['news']['title']}</h2>
                        <div class="news-content">
                            {d['news']['text']}
                        </div>
                    </div>
                </div>
            </div>
            <div class="quote">"{d['quote']}"</div>
            <div class="comic-wrapper">
                <img class="comic-img" src="{d['comic']['img_url']}">
            </div>
        </div>
    </body>
    </html>
    """
    
    print("Rendering PNG...")
    output_filename = 'newspaper.png'
    
    # 1. Save the HTML content to a physical file
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)
        
    # 2. Generate the absolute local file URL
    import os
    current_dir = os.path.abspath(os.path.dirname(__file__))
    file_url = f"file:///{os.path.join(current_dir, 'index.html').replace(chr(92), '/')}"
    
    # 3. Take the screenshot using the file URL, keeping your strict size!
    hti.screenshot(url=file_url, save_as=output_filename, size=(480, 800))
    
    print(f"Success! Saved to {output_filename}")

if __name__ == '__main__':
    generate_newspaper()