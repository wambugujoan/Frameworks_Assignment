import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud, STOPWORDS
from collections import Counter
import re

# Optional: improve plot aesthetics
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (10, 5)

# --- Load Data ---
@st.cache_data
def load_data():
    df = pd.read_csv("metadata_cleaned.csv")
    df['publish_year'] = pd.to_numeric(df['publish_year'], errors='coerce')
    return df

df = load_data()

# --- App Title & Description ---
st.title("CORD-19 Metadata Explorer")
st.markdown("""
Explore the CORD-19 research dataset interactively.  
Filter by publication year, view top journals, and visualize paper titles.
""")

# --- Interactive Widgets ---
# Year slider
min_year = int(df['publish_year'].min())
max_year = int(df['publish_year'].max())
year_range = st.slider("Select publication year range:", min_year, max_year, (min_year, max_year))

# Filter data by selected year range
df_filtered = df[(df['publish_year'] >= year_range[0]) & (df['publish_year'] <= year_range[1])]

# Dropdown for top N journals
top_n = st.selectbox("Select number of top journals to display:", [5, 10, 15, 20], index=1)

# --- Visualizations ---

# 1. Papers per year
papers_per_year = df_filtered['publish_year'].value_counts().sort_index()
st.subheader("Number of Publications per Year")
fig1, ax1 = plt.subplots()
sns.lineplot(x=papers_per_year.index, y=papers_per_year.values, marker="o", ax=ax1)
ax1.set_xlabel("Year")
ax1.set_ylabel("Number of Papers")
st.pyplot(fig1)

# 2. Top journals publishing COVID-19 papers
covid_df = df_filtered[
    df_filtered['abstract'].str.contains("COVID-19", case=False, na=False) |
    df_filtered['title'].str.contains("COVID-19", case=False, na=False)
]
top_journals = covid_df['journal'].value_counts().head(top_n)
st.subheader(f"Top {top_n} Journals Publishing COVID-19 Research")
fig2, ax2 = plt.subplots()
sns.barplot(x=top_journals.values, y=top_journals.index, palette="viridis", ax=ax2)
ax2.set_xlabel("Number of Papers")
ax2.set_ylabel("Journal")
st.pyplot(fig2)

# 3. Word Cloud of paper titles
titles_text = " ".join(df_filtered['title'].dropna().astype(str))
titles_text = re.sub(r'[^\w\s]', '', titles_text).lower()
wordcloud = WordCloud(
    width=800, height=400, background_color='white',
    stopwords=STOPWORDS, max_words=100
).generate(titles_text)

st.subheader("Word Cloud of Paper Titles")
fig3, ax3 = plt.subplots(figsize=(12,6))
ax3.imshow(wordcloud, interpolation='bilinear')
ax3.axis("off")
st.pyplot(fig3)

# 4. Show a sample of the data
st.subheader("Sample of the Dataset")
st.dataframe(df_filtered.sample(10))
