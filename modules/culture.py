import requests
import random
from PIL import Image
from io import BytesIO

def fetch_facts_module():
    url = "https://uselessfacts.jsph.pl/api/v2/facts/random?language=en"
    facts = []
    for _ in range(3):
        try:
            response = requests.get(url, timeout=3)
            # Catch Redis snapshot failures or invalid responses gracefully
            if response.status_code != 200 or "MISCONF Redis" in response.text:
                facts.append("The first modern alarm clock could only ring at 4 a.m.")
                continue
            facts.append(response.json().get("text", "Fact unavailable."))
        except Exception as e:
            print(f"Facts Iteration Error: {e}")
            facts.append("Vintage newspapers relied heavily on telegraph systems.")
    return facts

def fetch_word_module():
    # Fallback structure matching wordnik output format natively
    default_word = {"word": "Serendipity", "def": "The occurrence of events by chance in a happy way."}
    api_key = "YOUR_API_KEY" # Replace if you own a valid Wordnik registration string
    if api_key == "YOUR_API_KEY":
        return default_word

    try:
        url = f"https://api.wordnik.com/v4/words.json/wordOfTheDay?api_key={api_key}"
        data = requests.get(url, timeout=3).json()
        return {"word": data['word'], "def": data['definitions'][0]['text']}
    except Exception as e:
        print(f"Wordnik API Error: {e}")
        return default_word

def fetch_quote_module():
    try:
        data = requests.get("https://zenquotes.io/api/today", timeout=3).json()[0]
        return f"{data['q']} — {data['a']}"
    except Exception as e:
        print(f"Quotes API Error: {e}")
        return "Stay curious. — Unknown"

def fetch_fitting_xkcd():
    for _ in range(10):
        try:
            rid = random.randint(1, 2900)
            data = requests.get(f"https://xkcd.com/{rid}/info.0.json", timeout=3).json()
            img_res = requests.get(data['img'], timeout=3)
            img = Image.open(BytesIO(img_res.content))
            # Validate display aspect ratio match constraints
            if 1.5 <= (img.width / img.height) <= 3.0 and img.width <= 750:
                return {"title": data.get("title", "XKCD"), "img_url": data['img']}
        except Exception:
            continue
    return {"title": "Wisdom", "img_url": "https://imgs.xkcd.com/comics/wisdom_of_the_ancients.png"}