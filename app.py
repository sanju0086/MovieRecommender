import streamlit as st
import pickle
import pandas as pd
import requests

# Custom CSS for navbar and movie cards
st.markdown("""
<style>
/* Navbar style */
.navbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 15px 25px;
    background-color: #1f1f1f;
    color: white;
    border-radius: 10px;
    margin-bottom: 30px;
}
.nav-button {
    background-color: #ff4b4b;
    color: white;
    border: none;
    padding: 8px 18px;
    border-radius: 5px;
    cursor: pointer;
    margin-left: 10px;
    transition: 0.3s;
}
.nav-button:hover {
    background-color: #ff1a1a;
}

/* Movie card style */
.movie-card {
    padding: 15px;
    border-radius: 15px;
    text-align: center;
    transition: transform 0.3s, box-shadow 0.3s;
    box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    background-color: white;
    margin-bottom: 20px;
}
.movie-card:hover {
    transform: scale(1.05);
    box-shadow: 0 10px 25px rgba(0,0,0,0.2);
}
.movie-title {
    font-weight: bold;
    margin-top: 10px;
    color: #333333;
}
</style>
""", unsafe_allow_html=True)

# Navbar simulation
st.markdown("""
<div class="navbar">
    <div style="font-size:26px;font-weight:bold;">🎬 Movie Recommender</div>
    <div>
        <button class="nav-button" onclick="window.location.reload();">Home</button>
        <button class="nav-button" onclick="window.open('https://www.themoviedb.org', '_blank')">TMDb</button>
        <button class="nav-button" onclick="window.location.reload();">Refresh</button>
    </div>
</div>
""", unsafe_allow_html=True)

# Function to fetch poster with fallback
def fetch_poster(movie_id, movie_title):
    try:
        response = requests.get(
            f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=928ff1034abb6f722edd1716e6b7fa2a&language=en-US',
            timeout=5
        )
        data = response.json()
        if data.get('poster_path'):
            return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
        else:
            return f"https://via.placeholder.com/300x450.png?text={movie_title.replace(' ', '+')}"
    except requests.exceptions.RequestException:
        return f"https://via.placeholder.com/300x450.png?text={movie_title.replace(' ', '+')}"

# Recommend function
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []

    for i in movies_list:
        title = movies.iloc[i[0]].title
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(title)
        recommended_movies_posters.append(fetch_poster(movie_id, title))

    return recommended_movies[:4], recommended_movies_posters[:4]

# Load data
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Streamlit UI
st.title("🎬 Movie Recommender System")

selected_movie_name = st.selectbox('Select a Movie:', movies['title'].values)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)
    cols = st.columns(4)
    for idx, col in enumerate(cols):
        with col:
            st.markdown(f"""
                <div class="movie-card">
                    <img src="{posters[idx]}" width="200px" style="border-radius:10px"/>
                    <div class="movie-title">{names[idx]}</div>
                </div>
            """, unsafe_allow_html=True)
