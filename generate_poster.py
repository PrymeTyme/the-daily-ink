import os
from dotenv import load_dotenv
from html2image import Html2Image
from modules.movies import fetch_omdb_poster

load_dotenv()

def initialize_renderer():
    edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    if os.path.exists(edge_path):
        return Html2Image(browser_executable=edge_path)
    return Html2Image()

def main():
    print("Fetching movie data from OMDB...")
    movie_data = fetch_omdb_poster()
    
    if not movie_data:
        print("Failed to fetch movie data. Exiting.")
        return

    print(f"Selected Movie: {movie_data['title']} (Rating: {movie_data['rating']})")

    template_path = os.path.join(os.path.dirname(__file__), "templates", "poster.html")
    with open(template_path, "r", encoding="utf-8") as template_file:
        html_template = template_file.read()

    
    rendered_html = html_template.replace("{poster_url}", movie_data['poster_url'])
    rendered_html = rendered_html.replace("{movie_rating}", movie_data['rating'])

    hti = initialize_renderer()
    print("Rendering poster image...")
    hti.screenshot(
        html_str=rendered_html, 
        save_as='poster.png',
        size=(480, 800)
    )
    print("Successfully generated poster.png!")

if __name__ == "__main__":
    main()