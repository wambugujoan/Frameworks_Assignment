import pandas as pd

# === 1. Load the dataset ===
print("Loading dataset...")
df = pd.read_csv("metadata.csv")

# === 2. Basic info ===
print("\n=== Dataset Overview ===")
print(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}")
print("\nColumn names:")
print(df.columns.tolist())

# === 3. Check missing values ===
print("\n=== Missing Values (Top 10) ===")
print(df.isnull().sum().sort_values(ascending=False).head(10))

# === 4. Convert publish_time to datetime ===
df['publish_time'] = pd.to_datetime(df['publish_time'], errors='coerce')

# === 5. Key insights ===
print("\n=== Key Insights ===")

# Unique journals
print(f"Unique journals: {df['journal'].nunique()}")

# Most common journals (top 5)
print("\nTop 5 Journals by Paper Count:")
print(df['journal'].value_counts().head(5))

# Publication years
print("\nPublication Year Distribution:")
print(df['publish_time'].dt.year.value_counts().sort_index())

# Papers with abstracts vs without
with_abstract = df['abstract'].notnull().sum()
without_abstract = df['abstract'].isnull().sum()
print(f"\nPapers with abstracts: {with_abstract}")
print(f"Papers without abstracts: {without_abstract}")

# License distribution
print("\nLicense Distribution:")
print(df['license'].value_counts().head(10))

# === 6. Example filter: COVID-19 keyword search ===
covid_papers = df[df['abstract'].str.contains("COVID-19", na=False)]
print(f"\nNumber of papers mentioning 'COVID-19' in abstract: {len(covid_papers)}")

# === 7. Save cleaned summary ===
summary = {
    "rows": df.shape[0],
    "columns": df.shape[1],
    "unique_journals": df['journal'].nunique(),
    "papers_with_abstracts": int(with_abstract),
    "papers_without_abstracts": int(without_abstract),
    "papers_with_covid19_in_abstract": len(covid_papers)
}
pd.DataFrame([summary]).to_csv("metadata_summary.csv", index=False)

print("\n✅ Analysis complete! Results saved to metadata_summary.csv")
