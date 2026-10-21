import pandas as pd
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

movies = pd.read_csv("south_movies.csv")

movies["tags"] = (
    movies["genre"] + " " +
    movies["language"] + " " +
    movies["year"].astype(str)
)

cv = CountVectorizer(max_features=5000, stop_words="english")
vectors = cv.fit_transform(movies["tags"]).toarray()

similarity = cosine_similarity(vectors)

movie_matrix = pd.DataFrame(
    similarity,
    index=movies["title"],
    columns=movies["title"]
)

pickle.dump(movie_matrix, open("movie_matrix.pkl", "wb"))
pickle.dump(similarity, open("similarity.pkl", "wb"))

print("Telugu model trained successfully")