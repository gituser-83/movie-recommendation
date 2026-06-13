import streamlit as st
import pickle
import requests

st.set_page_config(
    page_title="CineMatch: Cyberpunk",
    page_icon="🦾",
    layout="wide",
    initial_sidebar_state="collapsed"
)

try:
    movies = pickle.load(open("movies.pkl", "rb"))
except FileNotFoundError:
    st.error("SYSTEM FAILURE: DATABASE NOT FOUND")
    st.stop()

def clean_genre(x):
    if isinstance(x, list): return x
    return [x] if isinstance(x, str) else []

def format_overview(x):
    if isinstance(x, list): return " ".join(x)
    return str(x) if x and str(x) != 'nan' else "ENCRYPTED DATA"

movies['genres'] = movies['genres'].apply(clean_genre)
all_genres = sorted(list(set([g for sublist in movies['genres'] for g in sublist])))

@st.cache_data(ttl=3600)
def get_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8"
    try:
        data = requests.get(url, timeout=1).json()
        if data.get('poster_path'):
            return f"https://image.tmdb.org/t/p/w500/{data['poster_path']}"
    except: pass
    return "https://images.unsplash.com/photo-1550745165-9bc0b252726f?q=80&w=500"

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;900&family=Rajdhani:wght@500;700&display=swap');
    
    .stApp {
        background-color: #050505;
        background-image: 
            linear-gradient(rgba(0, 255, 204, 0.05) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0, 255, 204, 0.05) 1px, transparent 1px);
        background-size: 30px 30px;
        color: #00ffcc;
        font-family: 'Rajdhani', sans-serif;
    }

    .cyber-header {
        text-align: center;
        padding: 50px 0;
        background: rgba(255, 0, 85, 0.1);
        border-bottom: 3px solid #ff0055;
        margin-bottom: 50px;
        box-shadow: 0 10px 30px rgba(255, 0, 85, 0.2);
    }
    
    .cyber-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 5.5rem;
        font-weight: 900;
        color: #fff;
        text-shadow: 2px 2px #ff0055, -2px -2px #00ffcc;
        letter-spacing: 8px;
    }

    div[data-testid="stSelectbox"] > div {
        background: #111 !important;
        border: 2px solid #00ffcc !important;
        border-radius: 0px !important;
        color: #00ffcc !important;
    }

    .stButton>button {
        width: 100%;
        background: #ff0055 !important;
        color: white !important;
        border: none !important;
        font-family: 'Orbitron' !important;
        font-weight: 700 !important;
        border-radius: 0px !important;
        height: 50px;
        transition: 0.2s;
        clip-path: polygon(5% 0%, 100% 0%, 95% 100%, 0% 100%);
    }
    
    .stButton>button:hover {
        background: #00ffcc !important;
        color: #000 !important;
        transform: skew(-2deg);
    }

    .card-container { perspective: 1000px; height: 520px; margin-bottom: 30px; }
    .card-checkbox { display: none; }
    .movie-card-inner {
        position: relative; width: 100%; height: 100%;
        transition: 0.6s; transform-style: preserve-3d; cursor: pointer;
    }
    .card-checkbox:checked + .movie-card-inner { transform: rotateY(180deg); }
    .card-front, .card-back {
        position: absolute; width: 100%; height: 100%;
        backface-visibility: hidden; border: 2px solid #333; background: #0a0a0a;
    }
    .card-front { border-left: 4px solid #00ffcc; }
    .card-back { transform: rotateY(180deg); padding: 25px; border: 2px solid #ff0055; }

    .poster-img { width: 100%; height: 380px; object-fit: cover; border-bottom: 1px solid #333; }
    .movie-name { color: #fff; font-family: 'Orbitron'; font-size: 1.1rem; padding: 15px 10px 5px; }
    .movie-meta { color: #ff0055; font-weight: 700; padding: 0 10px; font-size: 0.8rem; }
    .overview-text { color: #aaa; font-size: 0.9rem; margin-top: 15px; border-left: 2px solid #ff0055; padding-left: 10px; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="cyber-header">
        <h1 class="cyber-title">CINEMATCH</h1>
        <p style="letter-spacing: 10px; color: #ff0055; font-weight:700;">SECURE_LINE_CONNECTED</p>
    </div>
""", unsafe_allow_html=True)

_, col_mid, _ = st.columns([1, 2, 1])
with col_mid:
    selected_genre = st.selectbox("INTERFACE: SELECT_GENRE", all_genres)
    btn = st.button("RUN_SEARCH.exe")

if btn:
    filtered = movies[movies['genres'].apply(lambda x: selected_genre in x)]
    if 'vote_average' in filtered.columns:
        filtered = filtered.sort_values(by='vote_average', ascending=False)
    
    recs = filtered.head(12)
    st.markdown(f"<h3 style='font-family:Orbitron; border-bottom:1px solid #333; padding-bottom:10px;'>RESULTS_{selected_genre.upper()}</h3>", unsafe_allow_html=True)
    
    for row_idx in range(0, len(recs), 4):
        cols = st.columns(4)
        for col_idx in range(4):
            movie_idx = row_idx + col_idx
            if movie_idx < len(recs):
                movie = recs.iloc[movie_idx]
                m_id = getattr(movie, 'movie_id', 0)
                poster = get_poster(m_id)
                rating = f"RATING: {movie.vote_average}" if 'vote_average' in movie else "STATUS: UNKNOWN"
                
                with cols[col_idx]:
                    st.markdown(f"""
                        <div class="card-container">
                            <input type="checkbox" id="chk_{movie_idx}" class="card-checkbox">
                            <label for="chk_{movie_idx}" class="movie-card-inner">
                                <div class="card-front">
                                    <img src="{poster}" class="poster-img">
                                    <div class="movie-name">{movie.title.upper()}</div>
                                    <div class="movie-meta">{rating}</div>
                                </div>
                                <div class="card-back">
                                    <div style="font-family:Orbitron; color:#ff0055; font-size:0.7rem;">FILE_ACCESS_GRANTED</div>
                                    <div style="font-size:1.3rem; font-weight:700; color:#00ffcc; margin:10px 0; font-family:Orbitron;">{movie.title.upper()}</div>
                                    <p class="overview-text">{format_overview(getattr(movie, 'overview', ""))}</p>
                                    <div style="margin-top:auto; color:#ff0055; font-weight:700;">{rating}</div>
                                </div>
                            </label>
                        </div>
                    """, unsafe_allow_html=True)
else:
    st.markdown("<br><p style='text-align:center; color:#333; font-family:Orbitron;'>SYSTEM_IDLE: SELECT PARAMETERS</p>", unsafe_allow_html=True)