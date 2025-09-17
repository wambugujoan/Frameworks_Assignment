# Part 2: Data Cleaning and Preparation
# 3. Handle missing data

import pandas as pd

# Load metadata.csv
df = pd.read_csv("metadata.csv")

print(f"Initial shape: {df.shape}")

missing_counts = df.isnull().sum()
missing_percentage = (missing_counts / len(df)) * 100
missing_summary = pd.DataFrame({
    'missing_count': missing_counts,
    'missing_percentage': missing_percentage
}).sort_values(by='missing_percentage', ascending=False)

print(missing_summary.head(15))

# Drop columns with too many missing values
threshold = 70  # percent
cols_to_drop = missing_summary[missing_summary['missing_percentage'] > threshold].index
df_clean = df.drop(columns=cols_to_drop)

# Fill missing abstracts with empty string
df_clean['abstract'] = df_clean['abstract'].fillna("")

# Fill missing authors with 'Unknown'
df_clean['authors'] = df_clean['authors'].fillna("Unknown")

# Optional: Drop rows where publication date is missing
df_clean = df_clean.dropna(subset=['publish_time'])

# Part 2: Data Cleaning and Preparation
# 4. Prepare data for analysis
df_clean['publish_time'] = pd.to_datetime(df_clean['publish_time'], errors='coerce')

# Drop rows with invalid dates
df_clean = df_clean.dropna(subset=['publish_time'])

df_clean['publish_year'] = df_clean['publish_time'].dt.year

df_clean['abstract_word_count'] = df_clean['abstract'].apply(lambda x: len(str(x).split()))

df_clean['author_count'] = df_clean['authors'].apply(lambda x: len(str(x).split(';')))

df_clean.to_csv("metadata_cleaned.csv", index=False)
print(f"Cleaned dataset saved. Shape: {df_clean.shape}")
