# streamlit.py
import streamlit as st
from recommendation import recommend, movies

st.set_page_config(page_title="Movie Recommendation System", layout="wide")
st.title("🎬 Movie Recommendation System")

st.write("Select a movie you like and get 5 similar movie recommendations with posters!")

# =========================
# Movie selection dropdown
# =========================
selected_movie = st.selectbox(
    "Choose a movie:",
    list(movies['title'])
)

# =========================
# Recommendation button
# =========================
if st.button("Show Recommendations"):
    try:
        recommended_movies, recommended_posters = recommend(selected_movie)
        # Display recommendations in columns
        cols = st.columns(5)
        for col, movie, poster in zip(cols, recommended_movies, recommended_posters):
            col.image(poster, use_container_width=True)  # <-- changed here
            col.markdown(f"**{movie}**")


    except ValueError as e:
        st.error(str(e))
    except Exception as e:
        st.error("Something went wrong while fetching recommendations.")

