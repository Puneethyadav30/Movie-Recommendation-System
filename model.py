import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import pickle

# Load data
movies = pd.read_csv('movies.csv')
ratings = pd.read_csv('ratings.csv')

# Merge
data = ratings.merge(movies, on='movieId')

# Create pivot table
movie_user_matrix = data.pivot_table(index='title', columns='userId', values='rating').fillna(0)

# Similarity
similarity = cosine_similarity(movie_user_matrix)

# Save
pickle.dump(movie_user_matrix, open('movie_matrix.pkl', 'wb'))
pickle.dump(similarity, open('similarity.pkl', 'wb'))

print("Model created successfully!")