import streamlit as st
import pickle
import pandas as pd
import os
import gdown
st.set_page_config(
    page_title="Movie Recommender System",
    page_icon="popcorn_movie.jpg", #  custom logo/icon
    layout="wide"
)

def local_css(file_name):
    # This function reads .css file
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("style.css")

SIMILARITY_PKL_FILE_ID = "1gjj5dOnzGTxzUjq2nGptVTdQxJWUovnB"
SIMILARITY_PKL_PATH = 'similarity.pkl'

if not os.path.exists(SIMILARITY_PKL_PATH):
    st.info(f"Downloading large file: {SIMILARITY_PKL_PATH}...")
    try:
        # gdown downloads the file by ID and saves it locally
        gdown.download(id=SIMILARITY_PKL_FILE_ID, output=SIMILARITY_PKL_PATH, quiet=True, fuzzy=True)
        st.success(f"{SIMILARITY_PKL_PATH} downloaded successfully!")
    except Exception as e:
        st.error(f"Error downloading file with gdown: {e}")
        st.stop()

movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open(SIMILARITY_PKL_PATH, 'rb'))


# This line creates the final URL column that the function will use:

BASE_SEARCH_URL = 'https://www.google.com/search?q='
movies['movie_link'] = BASE_SEARCH_URL + movies['title'].str.replace(' ', '+')


def recommend(movie):
    movie_index = movies[movies['title']==movie].index[0]


    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True , key=lambda x:x[1])[1:6]

    recommended_data = []

    for i in movies_list:

        movie_data = movies.iloc[i[0]]

        recommended_data.append({
            'title': movie_data['title'],
            'link_url': movie_data['movie_link']
        })

    return recommended_data

st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
    'How would you like to see the recommendation?',
    movies['title'].values)

if st.button('Recommend'):
    recommendations = recommend(selected_movie_name)

    st.subheader(f"Top 5 Recommendations for **{selected_movie_name}**:")

    # Use Streamlit columns to display results horizontally
    cols = st.columns(5)  # Create 5 columns for the 5 posters
    FALLBACK_IMAGE_URL = 'https://via.placeholder.com/150x225.png?text=Movie+Link'

    for i, rec in enumerate(recommendations):
        with cols[i]:



            st.markdown(f"[{rec['title']}]({rec['link_url']})")

