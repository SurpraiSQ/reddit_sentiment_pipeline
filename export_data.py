import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

# --- Settings ---
load_dotenv()
DATABASE_URI = os.getenv("DATABASE_URI")

def export_to_excel():
    print("1. Connecting to DB")
    try:
        engine = create_engine(DATABASE_URI)
        
        # SQL quert
        query = "SELECT * FROM reddit_buildapc_sentiment ORDER BY created_date DESC"
        
        print("2. Downloading...")
        # pandas is sending SQL-query and making a table
        df = pd.read_sql(query, engine)
        
        if df.empty:
            print("Table is empty! Error is somewhere!!")
            return

        # 3. Save file
        filename = "buildapc_sentiment_report.csv"
        
        # encoding='utf-8-sig' for Excel
        df.to_csv(filename, index=False, encoding='utf-8-sig', sep=';')
        
        print(f"3. Great! Uploaded {len(df)} rows.")
        print(f"File '{filename}' is saved in same folder")
        
    except Exception as e:
        print(f"Error appiared: {e}")

if __name__ == "__main__":
    export_to_excel()