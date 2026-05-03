import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
 
NIFTY = "^NSEI"
GOLD = "GOLDBEES.NS"

START_DATE = (datetime.today() - timedelta(days=5*365)).strftime("%Y-%m-%d")
END_DATE = datetime.today().strftime("%Y-%m-%d")

VOL_THRESHOLD = -0.015 

#fetch data

def fetch_data(ticker):
    df = yf.download(ticker, start=START_DATE, end=END_DATE, auto_adjust=True)
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    df = df[['Close']]
    df.columns = [ticker]
    return df

def get_combined_data():
    nifty = fetch_data(NIFTY)
    gold = fetch_data(GOLD)

    df = nifty.join(gold, how='inner')
    df = df.iloc[30:]
    print(df.head())
    return df

# feature

def add_features(df):

    # Returns
    df['nifty_return'] = df[NIFTY].pct_change()
    df['gold_return'] = df[GOLD].pct_change()

    # Volatility
    df['nifty_vol_30d'] = df['nifty_return'].rolling(30).std()

    # RSI
    delta = df[NIFTY].diff()
    gain = delta.clip(lower=0).rolling(14).mean()
    loss = -delta.clip(upper=0).rolling(14).mean()
    rs = gain / loss
    df['nifty_rsi_14'] = 100 - (100 / (1 + rs))

    # High volatility flag
    df['high_vol_flag'] = df['nifty_return'] <= VOL_THRESHOLD

    # Gold behavior during crash
    df['gold_on_crash_days'] = np.where(
        df['high_vol_flag'],
        df['gold_return'],
        np.nan
    )

    return df

# main
def run_pipeline():
    df = get_combined_data()
    df = add_features(df)

    df.dropna(subset=['nifty_return', 'gold_return'], inplace=True)
    
    print(df['high_vol_flag'].value_counts())

    df.rename(columns={
    '^NSEI': 'nifty_price',
    'GOLDBEES.NS': 'gold_price'
    }, inplace=True)

    df.index.name = 'trade_date'

    df.to_csv("data/market_data.csv")

    print("Pipeline complete. Data saved to /data")

if __name__ == "__main__":
    run_pipeline()