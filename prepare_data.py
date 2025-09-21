# prepare_data.py
import pandas as pd
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os

# =========================
# CONFIG
# =========================
CSV_FILE = 'dataset.csv'        # your dataset file
PICKLE_MOVIES = 'movies_dict.pkl'
PICKLE_SIM = 'similarity.pkl'
FEATURE_COL = 'genre'         # column to compute similarity on (can also use 'description')

# =========================
# Load dataset
# =========================
if not os.path.exists(CSV_FILE):
    raise FileNotFoundError(f"Dataset file '{CSV_FILE}' not found!")

movies = pd.read_csv(CSV_FILE)

# Optional: fill NaNs in the feature column
movies[FEATURE_COL] = movies[FEATURE_COL].fillna('')

# =========================
# Compute similarity
# =========================
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(movies[FEATURE_COL])

similarity = cosine_similarity(tfidf_matrix)

# =========================
# Save pickles
# =========================
pickle.dump(movies.to_dict(), open(PICKLE_MOVIES, 'wb'))
pickle.dump(similarity, open(PICKLE_SIM, 'wb'))

print(f"Pickle files created successfully:\n- {PICKLE_MOVIES}\n- {PICKLE_SIM}")
