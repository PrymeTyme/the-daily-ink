import os
from datetime import datetime
from dotenv import load_dotenv
from html2image import Html2Image

# Import modular custom sub-packages
from modules.weather import get_weather
from modules.news import fetch_wiki_module, fetch_verge_module, fetch_history_module
from modules.culture import fetch_facts_module, fetch_word_module, fetch_quote_module, fetch_fitting_xkcd

load_dotenv()

def initialize_renderer():
    edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    if os.path.exists(edge_path):
        return Html2Image(browser_executable=edge_path)
    return Html2Image()

def generate_newspaper():
    print("Fetching dynamic data packages...")
    
    # Run API gather calls
    weather_data = get_weather()
    wiki = fetch_wiki_module()
    facts = fetch_facts_module()
    news = fetch_verge_module()
    history = fetch_history_module()
    word = fetch_word_module()
    quote = fetch_quote_module()
    comic = fetch_fitting_xkcd()
    
    # Process string interpolation elements
    facts_html = "".join([f"<li>{f}</li>" for f in facts])
    history_html = "".join([f'<div style="margin-bottom:8px;"><b>{item["year"]}</b>: {item["text"]}</div>' for item in history['items']])
    current_date = datetime.now().strftime("%A, %B %d, %Y - %H:%M").upper()

    print("Loading layout structures...")
    template_path = os.path.join(os.path.dirname(__file__), "templates", "layout.html")
    with open(template_path, "r", encoding="utf-8") as template_file:
        html_template = template_file.read()

    
    # Safely inject structured data variables using strict string replacement
    replacements = {
        "{date}": current_date,
        "{weather}": weather_data,
        "{wiki_title}": wiki['title'],
        "{wiki_text}": wiki['text'],
        "{history_title}": history['title'],
        "{history_items}": history_html,
        "{word_name}": word['word'],
        "{word_def}": word['def'],
        "{facts_list}": facts_html,
        "{news_title}": news['title'],
        "{news_text}": news['text'],
        "{quote_text}": quote,
        "{comic_url}": comic['img_url']
    }

    rendered_html = html_template
    for tag, value in replacements.items():
        rendered_html = rendered_html.replace(tag, str(value))

    print("Writing index working cache file...")
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(rendered_html)

    # Browser Execution Path Optimization Strategy
    hti = initialize_renderer()
    current_dir = os.path.abspath(os.path.dirname(__file__))
    file_url = f"file:///{os.path.join(current_dir, 'index.html').replace(chr(92), '/')}"

    print("Rendering newspaper snapshot output image via headless engine...")
    output_filename = 'newspaper.png'
    hti.screenshot(url=file_url, save_as=output_filename, size=(480, 800))
    print(f"Success! System generated output saved at: {output_filename}")

if __name__ == '__main__':
    generate_newspaper()