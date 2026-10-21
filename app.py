from flask import Flask, render_template, request
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import requests
app = Flask(__name__)
movies = pd.read_csv("south_movies.csv")
movies['genre'] = movies['genre'].fillna('')
cv = CountVectorizer(stop_words='english')
vectors = cv.fit_transform(movies['genre']).toarray()
similarity = cosine_similarity(vectors)
API_KEY = "fa469c663ae81b37a338084e34c876fe"
def fetch_poster(movie):
    try:
        url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={movie}"
        data = requests.get(url, timeout=5).json()
        if "results" in data and data["results"]:
            poster_path = data["results"][0].get("poster_path")
            if poster_path:
                return "https://image.tmdb.org/t/p/w500" + poster_path
    except:
        pass
    return "https://via.placeholder.com/300x450?text=No+Poster"
def recommend(movie):
    movie = movie.lower()

    matched = None
    for title in movies['title']:
        if movie in title.lower():
            matched = title
            break
    if matched is None:
        return [], []
    index = movies[movies['title'] == matched].index[0]
    distances = similarity[index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:10]
    names = []
    posters = []
    for i in movies_list:
        title = movies.iloc[i[0]].title
        names.append(title)
        posters.append(fetch_poster(title))
    return names, posters
@app.route("/", methods=["GET", "POST"])
def home():
    names = []
    posters = []
    if request.method == "POST":
        movie = request.form.get("movie")
        names, posters = recommend(movie)
    return render_template("index.html", names=names, posters=posters)
if __name__ == "__main__":
    app.run(debug=True)