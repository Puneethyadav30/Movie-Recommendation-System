import pandas as pd
import requests
import os
import time

API_KEY = "fa469c663ae81b37a338084e34c876fe"

# Load your dataset
movies = pd.read_csv(r"D:\Movie-Recommendation-System\south_movies.csv")

# Create folder
os.makedirs("static/posters", exist_ok=True)

def clean_name(title):
    title = title.lower()
    title = title.split("(")[0].strip()
    title = title.replace(" ", "_").replace(":", "").replace(".", "")
    return title

for movie in movies['title']:
    try:
        query = movie.split("(")[0].strip()

        url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={query}"
        data = requests.get(url).json()

        if "results" in data and data["results"]:
            poster_path = data["results"][0]["poster_path"]

            if poster_path:
                img_url = "https://image.tmdb.org/t/p/w500/" + poster_path
                img_data = requests.get(img_url).content

                filename = clean_name(movie) + ".jpg"

                with open(f"static/posters/{filename}", "wb") as f:
                    f.write(img_data)

                print(f"Downloaded: {movie}")

        time.sleep(0.3)  # avoid API limit

    except Exception as e:
        print(f"Error with {movie}: {e}")