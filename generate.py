import os
from datetime import datetime
from dotenv import load_dotenv
from html2image import Html2Image

from modules.weather import get_weather
from modules.news import fetch_wiki_module, fetch_verge_module, fetch_history_module, fetch_sports_module, fetch_good_news_module
from modules.culture import fetch_facts_module, fetch_word_module, fetch_fitting_xkcd, fetch_joke_module, fetch_quote_module, fetch_recipe_module, fetch_poem_module
from modules.finance import fetch_crypto_module

load_dotenv()

def initialize_renderer():
    edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    if os.path.exists(edge_path):
        return Html2Image(browser_executable=edge_path)
    return Html2Image()

def load_module_html(module_name):
    path = os.path.join("templates", "modules", f"{module_name}.html")
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def generate_newspaper():
    print("Fetching dynamic data packages...")
    
    # 1. Gather all data
    weather_data = get_weather()
    wiki = fetch_wiki_module()
    facts = fetch_facts_module()
    news = fetch_verge_module()
    history = fetch_history_module()
    word = fetch_word_module()
    comic = fetch_fitting_xkcd()
    crypto = fetch_crypto_module()
    sports = fetch_sports_module()
    joke = fetch_joke_module()
    quote_text = fetch_quote_module()
    recipe = fetch_recipe_module()
    poem = fetch_poem_module()
    good_news = fetch_good_news_module()
    
    # 2. Build list strings (The only logic needed before injection)
    facts_html = "".join([f"<li>{f}</li>" for f in facts])
    history_items = "".join([f'<div style="margin-bottom:8px;"><b>{item["year"]}</b>: {item["text"]}</div>' for item in history['items']])
    sports_items = "".join([f'<div style="margin-bottom:6px;"><b>{s["title"]}</b><br/><span style="font-weight:normal;">{s["summary"]}</span></div>' for s in sports])
    
    current_date = datetime.now().strftime("%A, %B %d, %Y").upper()

    # 3. Load & Inject modules
    # Every module is now a file in templates/modules/
    replacements = {
        "{date}": current_date,
        "{weather}": weather_data,
        "{crypto_btc}": crypto['btc'],
        "{crypto_eth}": crypto['eth'],
        "{wiki_block}": load_module_html("wiki").format(wiki_title=wiki['title'], wiki_text=wiki['text']),
        "{history_block}": load_module_html("history").format(history_title=history['title'], history_items=history_items),
        "{word_block}": load_module_html("word").format(word_name=word['word'], word_def=word['def']),
        "{facts_block}": load_module_html("facts").format(facts_list=facts_html),
        "{news_block}": load_module_html("news").format(news_title=news['title'], news_text=news['text']),
        "{sports_block}": load_module_html("sports").format(sports_items=sports_items),
        "{joke_block}": load_module_html("joke").format(joke_setup=joke['setup'], joke_punchline=joke['punchline']),
        "{quote_block}": load_module_html("quote").format(quote_text=quote_text),
        "{recipe_block}": load_module_html("recipe").format(recipe=recipe),
        "{poem_block}": load_module_html("poem").format(poem=poem),
        "{comic_url}": comic['img_url'],
        "{goodnews_block}": load_module_html("goodnews").format(good_news_title=good_news['title'], good_news_text=good_news['text']),
    }

    # 4. Assemble final page
    with open("templates/layout.html", "r", encoding="utf-8") as f:
        rendered_html = f.read()

    for tag, value in replacements.items():
        rendered_html = rendered_html.replace(tag, str(value))

    # 5. Render
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(rendered_html)
    
    

    # Browser Execution
    hti = initialize_renderer()
    current_dir = os.path.abspath(os.path.dirname(__file__))
    file_url = f"file:///{os.path.join(current_dir, 'index.html').replace(chr(92), '/')}"

    print("Rendering newspaper snapshot...")
    output_filename = 'newspaper.png'
    hti.screenshot(url=file_url, save_as=output_filename, size=(480, 800))
    print(f"Success! Output saved at: {output_filename}")

if __name__ == '__main__':
    generate_newspaper()