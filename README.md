# 🎵 LyricQuest

**LyricQuest** is a hybrid song search engine that allows users to search for songs based on **phrases from lyrics**, while also factoring in **song title relevance** and **user feedback (likes/dislikes)** to rank results.

> 🎓 *End semester project for the course - 20XW86 Information Retrieval Lab*

---

## 🚀 Features

- 🔍 **Lyrics + Title Based Search**  
  Search songs using a phrase from the lyrics. Relevance is calculated using both **lyrics** and **title** similarity.

- 📊 **Feedback-Based Ranking**  
  Incorporates user interactions (likes/dislikes) into the result ranking, making it adaptive and user-personalized.

- ⚖️ **Alpha-Beta Ranking Model**  
  A flexible formula that balances similarity and user feedback:
  ```
  similarity_score = α * title_sim + (1 - α) * lyrics_sim  
  final_score = β * similarity_score + (1 - β) * normalized_feedback
  ```

- 🎥 **YouTube Integration**  
  Displays playable YouTube videos for the songs shown.

- 👍 👎 **Like/Dislike System**  
  Users can provide feedback to influence future search rankings.

- 🌐 **Streamlit Interface**  
  Fully interactive web-based interface built using Streamlit.

---

## 🛠️ Technologies Used

- **Python**: Core backend
- **Streamlit**: User interface
- **MySQL**: Database for songs and feedback
- **Pandas / NumPy / Scikit-learn**: Data processing and TF-IDF calculations
- **NLTK**: Text processing (tokenization, stemming)
- **BeautifulSoup (BS4)**: YouTube video scraping
- **Pickle**: Stores precomputed matrices
- **Git**: Version control

---

## 📦 Installation

Follow these steps to set up LyricQuest locally:

1. **Clone the Repository**

```bash
git clone https://github.com/kanxshkk/LyricQuest-v2.git
cd LyricQuest-v2
```

2. **Install Required Packages**

```bash
pip install -r requirements.txt
```

3. **Configure MySQL Connection**

Open `app.py` and edit the `connect_to_db()` function with your credentials.

4. **Generate Precomputed Data**

Run the scripts inside the `utils/` directory to generate `precomputed_data.pkl`.

5. **Run the App**

```bash
streamlit run app.py
```

---

## ⚙️ Working Details

### 🎯 Ranking Formula

- **Title-Lyrics Similarity:**

```
similarity_score = α * title_sim + (1 - α) * lyrics_sim
```

- **Final Score with Feedback:**

```
final_score = β * similarity_score + (1 - β) * normalized(net_likes - net_dislikes)
```

> Songs with no feedback default to a neutral value of **0.5** for fairness.

### 🔁 Feedback Handling

- Likes and dislikes are stored per `(user_query, song_id)` pair.
- Normalized preference is used to update scores without bias from outliers.

---

## 👥 Contributors

- 21PW10  
- 21PW15  
- 21PW22  

---

## 📌 Notes

- Ensure you create your MySQL database with
```bash
CREATE TABLE user_interactions (
    interaction_id INT AUTO_INCREMENT PRIMARY KEY,
    query VARCHAR(255) NOT NULL,
    song_id INT,
    like_count INT DEFAULT 0,
    dislike_count INT DEFAULT 0,
);
```
- The app uses BeautifulSoup to fetch YouTube video links — a working internet connection is required.
- You can tune `alpha` and `beta` from the sidebar in the Streamlit interface for experimentation.

---
