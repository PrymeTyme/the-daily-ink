import os
import requests
import random

def fetch_omdb_poster():
    api_key = os.getenv("OMDB_API_KEY")
    if not api_key:
        print("Error: No OMDB_API_KEY found.")
        return None

    movie_pool = [
        "Blade Runner", "The Matrix", "Interstellar", "Alien", 
        "Jurassic Park", "The Godfather", "Pulp Fiction", "Dune",
        "The Dark Knight", "Inception", "Fight Club", "Goodfellas",
        "The Truman Show", "Spirited Away", "Mad Max: Fury Road"
    ]
    
    selected_movie = random.choice(movie_pool)
    url = f"http://www.omdbapi.com/?t={selected_movie}&apikey={api_key}"
    
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            
            if data.get("Response") == "True" and data.get("Poster") != "N/A":
                return {
                    "title": data.get("Title", "Unknown"), 
                    "poster_url": data.get("Poster"),
                    "rating": data.get("imdbRating", "N/A") 
                }
            else:
                print(f"OMDB error or no poster available for: {selected_movie}")
    except Exception as e:
        print(f"OMDB API Error: {e}")
        
    return None