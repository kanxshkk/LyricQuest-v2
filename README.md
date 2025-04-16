# 🎵 LyricQuest

LyricQuest is a hybrid song search engine that allows users to search for songs based on **phrases from lyrics**, while also factoring in **song title relevance** and **user feedback (likes/dislikes)** to rank results. This is the end semester project for the course - 20XW86 Information Retrieval Lab.

---

## 🚀 Features

- 🔍 **Lyrics + Title Based Search**: Users can search for songs using a line or phrase from the lyrics. The engine computes a weighted similarity using both the song **title** and **lyrics**.
- 📊 **Feedback-Based Ranking**: Results are ranked not just by similarity, but also by **user interactions** (likes/dislikes). This makes search results adaptive to user preferences.
- 📈 **Alpha-Beta Ranking Model**: Uses a customizable scoring formula:

- 🎥 **YouTube Integration**: Displays a playable YouTube video for each recommended song.
- 👍 👎 **User Interaction**: Users can like or dislike any song to improve future rankings for that specific search query.
- 🌐 **Streamlit Interface**: Interactive, web-based frontend using Streamlit.

---

## 🛠️ Technologies Used

- **Python**: Core backend and logic
- **Streamlit**: UI development
- **MySQL**: Persistent storage for song data and user feedback
- **Pandas, NumPy, Scikit-learn**: Data processing and similarity computations
- **NLTK**: Text preprocessing (stemming, tokenization)
- **BeautifulSoup (BS4)**: YouTube video scraping
- **Pickle**: For storing precomputed TF-IDF matrices
- **Git**: Version control

---

## 📦 Installation

To run LyricQuest locally:

1. Clone the repository:


```git clone https://github.com/kanxshkk/LyricQuest.git
cd LyricQuest```

2. Install dependencies:

```pip install -r requirements.txt```

3. Set up the MySQL database and configure credentials in app.py under connect_to_db() function.

4. Run the utils/ scripts (provided in the repo) to generate the required precomputed_data.pkl.

5. Launch the application:
```streamlit run app.py```


**Working**
1. Alpha-Beta Weighted Ranking Model
α controls how much importance is given to title vs lyrics:

similarity_score = α * title_sim + (1 - α) * lyrics_sim

β controls how much importance is given to similarity vs user feedback:

final_score = β * similarity_score + (1 - β) * normalized(net_likes - net_dislikes)

2. Feedback Handling
Each song-query pair is tracked.

Normalized feedback (net_likes - net_dislikes) is used for ranking.

For songs without feedback, a default value of 0.5 is used




**Contributors**
21PW10

21PW15

21PW22