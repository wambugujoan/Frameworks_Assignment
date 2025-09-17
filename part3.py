import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud, STOPWORDS  # <-- Import STOPWORDS
from collections import Counter
import re

# Optional: improve plot aesthetics
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

# Load cleaned dataset
df = pd.read_csv("metadata_cleaned.csv")
print(df.head())

# --- Papers per year ---
papers_per_year = df['publish_year'].value_counts().sort_index()
print(papers_per_year)

# --- Top journals publishing COVID-19 papers ---
covid_df = df[
    df['abstract'].str.contains("COVID-19", case=False, na=False) |
    df['title'].str.contains("COVID-19", case=False, na=False)
]
top_journals = covid_df['journal'].value_counts().head(10)
print(top_journals)

# --- Most frequent words in titles ---
# Combine all titles, safely handling missing values
titles_text = " ".join(df['title'].dropna().astype(str))

# Remove punctuation and lowercase
titles_text = re.sub(r'[^\w\s]', '', titles_text).lower()

# Split into words and remove stopwords
words = [word for word in titles_text.split() if word not in STOPWORDS]

# Count frequency
word_counts = Counter(words)
most_common_words = word_counts.most_common(20)
print(most_common_words)

# --- Plot number of publications over time ---
plt.figure(figsize=(12,6))
sns.lineplot(x=papers_per_year.index, y=papers_per_year.values, marker="o")
plt.title("Number of Publications per Year")
plt.xlabel("Year")
plt.ylabel("Number of Papers")
plt.xticks(rotation=45)
plt.show()

# --- Bar chart of top journals ---
plt.figure(figsize=(12,6))
sns.barplot(x=top_journals.values, y=top_journals.index, palette="viridis")
plt.title("Top 10 Journals Publishing COVID-19 Research")
plt.xlabel("Number of Papers")
plt.ylabel("Journal")
plt.show()

# --- Word Cloud of paper titles ---
wordcloud = WordCloud(
    width=800, height=400, background_color='white',
    stopwords=STOPWORDS, max_words=100
).generate(titles_text)

plt.figure(figsize=(15,7))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.title("Word Cloud of Paper Titles")
plt.show()

# --- Distribution of paper counts by license/source ---
top_sources = df['license'].fillna("Unknown").value_counts().head(10)

plt.figure(figsize=(12,6))
sns.barplot(x=top_sources.values, y=top_sources.index, palette="magma")
plt.title("Top Paper Sources / License Types")
plt.xlabel("Number of Papers")
plt.ylabel("License / Source")
plt.show()
