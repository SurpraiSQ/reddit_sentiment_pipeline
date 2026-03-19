import requests
import pandas as pd
from textblob import TextBlob
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

# --- Settings ---
load_dotenv()
DATABASE_URI = os.getenv("DATABASE_URI")

def fetch_reddit_data():
    print("1. Extracting from r/buildapc")
    url = "https://www.reddit.com/r/buildapc/new.json?limit=25"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) ETL-Pet-Project"}
    
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Error API: {response.status_code}")
        return None
    
    data = response.json()
    raw_data = []
    for post in data['data']['children']:
        item = post['data']
        raw_data.append({
            "title": item['title'],
            "author": item['author'],
            "post_url": f"https://www.reddit.com{item['permalink']}",
            "created_utc": item['created_utc']
        })
    return pd.DataFrame(raw_data)

def transform_data(df):
    print("2. Transform and AI")
    # Convert date
    df['created_date'] = pd.to_datetime(df['created_utc'], unit='s')
    df = df.drop(columns=['created_utc'])
    
    # Function AI
    def get_sentiment(text):
        score = TextBlob(text).sentiment.polarity
        if score > 0.1: return 'Positive'
        elif score < -0.1: return 'Negative'
        else: return 'Neutral'
            
    df['sentiment_score'] = df['title'].apply(lambda x: TextBlob(x).sentiment.polarity)
    df['sentiment_label'] = df['title'].apply(get_sentiment)
    return df

def load_to_db(df, uri):
    print("3. Loading to DB")
    try:
        # Create connection
        engine = create_engine(uri)
        
        # pandas loading 
        # if_exists='append' - adding new rows
        df.to_sql('reddit_buildapc_sentiment', engine, if_exists='append', index=False)
        print(f"Great! {len(df)} rows added to DB.")
    except Exception as e:
        print(f"Error: {e}")

# --- Pipeline start ---
if __name__ == "__main__":
    df_raw = fetch_reddit_data()
    if df_raw is not None:
        df_clean = transform_data(df_raw)
        load_to_db(df_clean, DATABASE_URI)