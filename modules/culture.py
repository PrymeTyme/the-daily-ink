import requests
import random
from PIL import Image
from io import BytesIO
import xml.etree.ElementTree as ET

def fetch_facts_module():
    url = "https://uselessfacts.jsph.pl/api/v2/facts/random?language=en"
    facts = []
    for _ in range(2):
        try:
            response = requests.get(url, timeout=3)
            
            if response.status_code != 200 or "MISCONF Redis" in response.text:
                facts.append("The first modern alarm clock could only ring at 4 a.m.")
                continue
            facts.append(response.json().get("text", "Fact unavailable."))
        except Exception as e:
            print(f"Facts Iteration Error: {e}")
            facts.append("Vintage newspapers relied heavily on telegraph systems.")
    return facts

def fetch_word_module():
    """Fetches a definition for a random word of the day."""
    
    word_list = ["serendipity", "ephemeral", "luminous", "resilience", "eloquent"]
    word = random.choice(word_list)
    
    try:
        url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
        data = requests.get(url, timeout=3).json()
        
        
        definition = data[0]['meanings'][0]['definitions'][0]['definition']
        return {"word": word.capitalize(), "def": definition}
    except:
        return {"word": "Serendipity", "def": "The occurrence of events by chance in a happy way."}

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

def fetch_joke_module():
    url = "https://official-joke-api.appspot.com/random_joke"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            return {"setup": data['setup'], "punchline": data['punchline']}
    except Exception as e:
        print(f"Joke API Error: {e}")
    return {"setup": "Why do programmers prefer dark mode?", "punchline": "Because light attracts bugs."}

import requests

def fetch_recipe_module():
    """Fetches a random recipe and formats its ingredient list from TheMealDB."""
    try:
        response = requests.get("https://www.themealdb.com/api/json/v1/1/random.php", timeout=5)
        data = response.json()["meals"][0]
        
        title = data["strMeal"]
        category = data["strCategory"]
        
       
        ingredients = []
        for i in range(1, 21):
            ingredient = data.get(f"strIngredient{i}")
            measure = data.get(f"strMeasure{i}")
            
            
            if ingredient and ingredient.strip():
                
                measure_text = measure.strip() if measure else ""
                ingredients.append(f"{measure_text} {ingredient.strip()}")
        
        
        ingredients_html = "".join([f"<li>{item}</li>" for item in ingredients])
        
        
        output = f"""
        <div style="font-weight:700; text-align:center; font-family:'Oswald', sans-serif; margin-bottom:6px;">
            {title} ({category})
        </div>
        <ul style="margin: 0; padding-left: 15px; font-size: 11px;">
            {ingredients_html}
        </ul>
        """
        
        return output
        
    except Exception as e:
        print(f"Recipe API Error: {e}")
        return "Kitchen closed for maintenance."

def fetch_poem_module():
    """Fetches a random classic poem from PoetryDB."""
    try:
        
        response = requests.get("https://poetrydb.org/random", timeout=5)
        data = response.json()[0] 
        
        title = data.get("title", "Unknown")
        author = data.get("author", "Unknown")
        
        lines = " / ".join(data.get("lines", [])[:8]) 
        
        return f"<b>{title}</b><br>by {author}<br><i style='font-size:10px;'>{lines}...</i>"
        
    except Exception as e:
        print(f"Poem API Error: {e}")
        return "<i>Poetry is currently unavailable.</i>"    