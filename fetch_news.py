import requests
import pandas as pd
from textblob import TextBlob
from datetime import datetime

API_KEY = "57463734dffc9dab773bb476ba7e60f6"   
KEYWORDS = ["technology", "AI"]
NEWS_URL = "https://gnews.io/api/v4/search"
output_file = "realtime_news.csv"

query = " OR ".join(KEYWORDS)  
params = {
    "q": query,
    "lang": "en",
    "max": 50,     
    "token": API_KEY
}

response = requests.get(NEWS_URL, params=params)
if response.status_code != 200:
    print("API request failed:", response.text)
    exit()

articles = response.json().get("articles", [])
if not articles:
    print("No articles found for keywords:", query)
    exit()

data = []
for article in articles:
    title = article.get("title", "")
    description = article.get("description", "")
    content = f"{title} {description}"
    timestamp = article.get("publishedAt")

    sentiment = TextBlob(content).sentiment.polarity
    keyword_count = sum(content.lower().count(k.lower()) for k in KEYWORDS)

    data.append({
        "timestamp": datetime.fromisoformat(timestamp.replace("Z", "+00:00")),
        "sentiment_score": sentiment,
        "keyword_count": keyword_count
    })

df = pd.DataFrame(data)
df["date"] = df["timestamp"].dt.date

df_daily = df.groupby("date").agg({
    "sentiment_score": "mean",
    "keyword_count": "sum"
}).reset_index()

df_daily.rename(columns={"date": "timestamp"}, inplace=True)

try:
    existing = pd.read_csv(output_file)
    existing["timestamp"] = pd.to_datetime(existing["timestamp"]).dt.date
    df_combined = pd.concat([existing, df_daily])
    df_combined = df_combined.drop_duplicates(subset=["timestamp"]).sort_values("timestamp")
except FileNotFoundError:
    df_combined = df_daily

if len(df_combined) < 2:
    last_row = df_combined.iloc[-1].copy()
    last_row['timestamp'] = (pd.to_datetime(last_row['timestamp']) - pd.Timedelta(days=1)).date()
    df_combined = pd.concat([df_combined, pd.DataFrame([last_row])])
    print("⚠️ Added a dummy previous day for testing Prophet.")

df_combined.to_csv(output_file, index=False)
print(f"✅ Daily aggregated news appended to {output_file}")
print(df_combined)
