import streamlit as st
import pickle
import pandas as pd
import os
import requests


def download_file(url,filename):
    if not os.path.exists(filename):
        st.info("Downloading file: {filename}")

        response = requests.get(url, stream=True)
        with open(filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk: f.write(chunk)
        st.success("Downloaded file: {filename}")
    return filename

SIMILARITY_PKL_URL = "https://drive.google.com/uc?export=download&id=1gjj5dOnzGTxzUjq2nGptVTdQxJWUovnB"

movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity_pkl_path = download_file(SIMILARITY_PKL_URL, "similarity.pkl")
similarity = pickle.load(open('similarity.pkl', 'rb'))


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
            # Display the poster image using the URL

            # Display the title as a clickable link
            st.markdown(f"[{rec['title']}]({rec['link_url']})")

            # Since we don't have a poster URL, we display a placeholder image
            # This is the best visual substitute for a missing poster.

