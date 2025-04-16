import streamlit as st
import mysql.connector
import re
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from nltk.stem import PorterStemmer
from services.youtube_crawler_service import youtube_crawler_service
import pickle
import os

# --- MySQL Connection ---
def connect_to_db():
    return mysql.connector.connect(
        user='root',
        password='',
        host='localhost',
        database='lyricquest'
    )

cnx = connect_to_db()
cursor = cnx.cursor()

# --- Load Precomputed Data ---
with open('utils/precomputed_data.pkl', 'rb') as f:
    (
        lyrics_vocabulary, lyrics_idf, tfidf_lyrics_df,
        title_vocabulary, title_idf, tfidf_title_df
    ) = pickle.load(f)

# --- Utility Functions ---
def tokenize(text):
    ps = PorterStemmer()
    return ' '.join([
        ps.stem(re.sub('[^a-zA-Z0-9]', '', word).lower())
        for word in text.split() if word
    ])

def create_query_df(query_dict, idf):
    df = pd.DataFrame([query_dict])
    df = df.div(df.sum(axis=1), axis=0)
    df = df.mul(idf, axis=1)
    return df.fillna(0)

def vectorize(df):
    return np.array(df.iloc[0]).reshape(1, -1)

# --- Interaction Handling ---
def update_interaction(query, title, song_id, is_like=True):
    column = 'like_count' if is_like else 'dislike_count'
    cursor.execute(
        f"SELECT id, {column} FROM user_interactions WHERE query = %s AND song_id = %s",
        (query, song_id)
    )
    entry = cursor.fetchone()

    if entry:
        interaction_id, count = entry
        cursor.execute(
            f"UPDATE user_interactions SET {column} = %s WHERE id = %s",
            (count + 1, interaction_id)
        )
    else:
        cursor.execute(
            f"INSERT INTO user_interactions (query, title, song_id, {column}) VALUES (%s, %s, %s, 1)",
            (query, title, song_id)
        )
    cnx.commit()

# --- Load Dataset ---
df = pd.read_csv('./irpackage.csv')
df.dropna(inplace=True)
df.set_index('Unnamed: 0', inplace=True)

# --- Streamlit UI ---
st.title("🎵 LyricQuest - A Song Search Engine")
query_input = st.text_input('', placeholder='Enter phrases of lyrics')
num_results = st.number_input('Number of results', min_value=5, max_value=20, step=1, format='%d')
alpha = st.slider("Similarity: Title vs Lyrics (alpha)", 0.0, 1.0, 0.2  )
beta = st.slider("Ranking: Similarity vs Feedback (beta)", 0.0, 1.0, 0.8)

if st.button("Find the song", type='primary') and query_input:
    query = tokenize(query_input)

    query_title_dict = dict.fromkeys(title_vocabulary, 0)
    query_lyrics_dict = dict.fromkeys(lyrics_vocabulary, 0)

    for term in query.split():
        if term in query_title_dict: query_title_dict[term] += 1
        if term in query_lyrics_dict: query_lyrics_dict[term] += 1

    query_title_vector = vectorize(create_query_df(query_title_dict, title_idf))
    query_lyrics_vector = vectorize(create_query_df(query_lyrics_dict, lyrics_idf))

    sim_scores = []
    net_prefs = []
    has_feedback_flags = []

    for i in range(len(tfidf_lyrics_df)):
        title_vector = vectorize(tfidf_title_df.iloc[[i]])
        lyrics_vector = vectorize(tfidf_lyrics_df.iloc[[i]])

        title_sim = cosine_similarity(query_title_vector, title_vector)[0][0]
        lyrics_sim = cosine_similarity(query_lyrics_vector, lyrics_vector)[0][0]
        sim_score = alpha * title_sim + (1 - alpha) * lyrics_sim

        cursor.execute(
            "SELECT like_count, dislike_count FROM user_interactions WHERE query = %s AND song_id = %s",
            (query, i)
        )
        entry = cursor.fetchone()
        if entry:
            net_pref = entry[0] - entry[1]
            has_feedback = True
        else:
            net_pref = 0
            has_feedback = False

        sim_scores.append(sim_score)
        net_prefs.append(net_pref)
        has_feedback_flags.append(has_feedback)

    # --- Normalize Feedback ---
    min_pref = min(net_prefs)
    max_pref = max(net_prefs)
    range_pref = max(max_pref - min_pref, 1e-5)

    final_scores = []
    for i in range(len(sim_scores)):
        sim = sim_scores[i]
        net = net_prefs[i]
        has_feedback = has_feedback_flags[i]

        norm_pref = (net - min_pref) / range_pref if has_feedback else 0.5
        final_score = beta * sim + (1 - beta) * norm_pref
        final_scores.append((i, final_score))

    sorted_results = sorted(final_scores, key=lambda x: -x[1])

    # --- Show Results ---
    results_shown = 0
    for idx, score in sorted_results:
        if score == 0 and results_shown == 0:
            st.warning('No lyrics found! Try with different phrases.')
            break

        song_data = df.iloc[idx]
        st.subheader(f"{song_data['title']} - {song_data['artist']}")
        st.write(song_data)
        st.markdown(
            youtube_crawler_service.GetYtVideo(f"{song_data['title']} video song {song_data['artist']}"),
            unsafe_allow_html=True
        )

        st.button("👍", key=f'like{idx}', on_click=update_interaction, args=(query, song_data['title'], idx, True))
        st.button("👎", key=f'dislike{idx}', on_click=update_interaction, args=(query, song_data['title'], idx, False))

        results_shown += 1
        if results_shown >= num_results:
            break
