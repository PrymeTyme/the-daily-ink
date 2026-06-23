import os
import base64
import requests
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

    # THE FIX: Download the image in Python and convert to Base64 text
    print("Downloading high-res poster...")
    img_response = requests.get(movie_data['poster_url'])
    img_base64 = base64.b64encode(img_response.content).decode('utf-8')
    base64_string = f"data:image/jpeg;base64,{img_base64}"

    template_path = os.path.join(os.path.dirname(__file__), "templates", "poster.html")
    with open(template_path, "r", encoding="utf-8") as template_file:
        html_template = template_file.read()

    # Inject the base64 string instead of the URL
    rendered_html = html_template.replace("{poster_url}", base64_string)
    rendered_html = rendered_html.replace("{movie_rating}", movie_data['rating'])

    # Render exactly to the Pi's 480x800 resolution
    hti = initialize_renderer()
    print("Rendering poster image...")

    # 1. Save the HTML content to a dedicated physical file
    poster_index_path = os.path.join(os.path.dirname(__file__), "poster_index.html")
    with open(poster_index_path, "w", encoding="utf-8") as f:
        f.write(rendered_html)
        
    # 2. Generate the absolute local file URL (replacing backslashes for cross-platform safety)
    import os
    absolute_path = os.path.abspath(poster_index_path)
    file_url = f"file:///{absolute_path.replace(chr(92), '/')}"
    
    # 3. Take the screenshot using the absolute URL, keeping your strict size!
    hti.screenshot(
        url=file_url, 
        save_as='poster.png',
        size=(480, 800)
    )
    print("Successfully generated poster.png!")

if __name__ == "__main__":
    main()