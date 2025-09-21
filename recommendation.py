# recommendation.py
import pickle
import pandas as pd
import requests
import os

# =========================
# Paths to pickle files
# =========================
BASE_DIR = os.path.dirname(__file__)
MOVIES_PICKLE = os.path.join(BASE_DIR, 'movies_dict.pkl')
SIMILARITY_PICKLE = os.path.join(BASE_DIR, 'similarity.pkl')

# =========================
# Load movie data
# =========================
if not os.path.exists(MOVIES_PICKLE) or not os.path.exists(SIMILARITY_PICKLE):
    raise FileNotFoundError(
        f"Pickle files not found. Make sure '{MOVIES_PICKLE}' and '{SIMILARITY_PICKLE}' exist."
    )

movies_dict = pickle.load(open(MOVIES_PICKLE, 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open(SIMILARITY_PICKLE, 'rb'))

# =========================
# Function to fetch poster
# =========================
def fetch_poster(title):
    """
    Fetch movie poster from OMDb API.
    Returns a default image if not found.
    """
    api_key = "2e543cf3"  # replace with your OMDb API key
    url = f"http://www.omdbapi.com/?t={title}&apikey={api_key}"
    try:
        response = requests.get(url).json()
        poster_url = response.get("Poster", None)
        if poster_url and poster_url != "N/A":
            return poster_url
    except:
        pass
    # Default image if not found
    return "https://cdn-icons-png.flaticon.com/512/1179/1179120.png"

# =========================
# Recommendation function
# =========================
def recommend(movie_name, n_recommendations=5):
    """
    Recommend movies similar to the given movie.
    
    Args:
        movie_name (str): Name of the movie.
        n_recommendations (int): Number of recommendations to return.
        
    Returns:
        recommended_movies (list of str)
        recommended_posters (list of str)
    """
    if movie_name not in movies['title'].values:
        raise ValueError(f"Movie '{movie_name}' not found in dataset.")

    # Find movie index
    index = movies[movies['title'] == movie_name].index[0]

    # Get similarity scores and sort
    distances = sorted(
        list(enumerate(similarity[index])),
        reverse=True,
        key=lambda x: x[1]
    )

    recommended_movies = []
    recommended_posters = []

    # Get top n recommendations (skip the first one, which is the movie itself)
    for i in distances[1:n_recommendations+1]:
        idx = i[0]
        title = movies.iloc[idx]['title']
        recommended_movies.append(title)
        recommended_posters.append(fetch_poster(title))

    return recommended_movies, recommended_posters

