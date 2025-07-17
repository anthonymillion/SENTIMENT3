import streamlit as st
import pandas as pd
import datetime

# Define symbol groups
stocks = ["NVDA", "MSFT", "AAPL", "AMZN", "GOOGL", "GOOG", "META", "TSLA", "AVGO", "COST", "AMD", "NFLX"]
indices = ["SP500", "QQQ", "USTECH100", "RUSSELL", "NIKKEI"]
commodities = ["GOLD", "USOIL", "BRENT", "COPPER", "SILVER", "NATGAS"]
currencies = ["USDJPY", "EURUSD", "DXY", "BTCUSD"]
volatility = ["VIX", "BONDYIELDS"]

# Timeframes including M15, M30
timeframes = ["1s", "5s", "15s", "30s", "M1", "M2", "M3", "M4", "M10", "M15", "M30", "H6", "H7", "H8", "1H", "4H", "Daily", "Weekly", "Monthly"]

# App title
st.set_page_config(page_title="AI EdgeFinder Final", layout="wide")
st.title("📊 AI EdgeFinder – Auto Sentiment Final")

# Select timeframe for main signal board
main_tf = st.selectbox("Select Main Timeframe", timeframes, index=10, key="main_tf")

# Select timeframe for Top Movers
top_tf = st.selectbox("Select Timeframe for Top Movers", timeframes, index=10, key="top_tf")

# Score and classify
def simulate_score(symbol, tf):
    base = (hash(symbol + tf + str(datetime.date.today())) % 9) - 4
    return round(base + (hash(tf) % 3 - 1), 2)

def classify_sentiment(score):
    if score > 1.5:
        return "🟢 Bullish"
    elif score < -1.5:
        return "🔴 Bearish"
    return "🟡 Neutral"

# Score all assets for main view
def score_group(symbols, tf):
    data = []
    for sym in symbols:
        score = simulate_score(sym, tf)
        sentiment = classify_sentiment(score)
        data.append({"Symbol": sym, "Score": score, "Sentiment": sentiment})
    return pd.DataFrame(data)

# Score Top Movers
top_movers = []
for sym in stocks:
    score = simulate_score(sym, top_tf)
    sentiment = classify_sentiment(score)
    if sentiment in ["🟢 Bullish", "🔴 Bearish"]:
        top_movers.append({"Symbol": sym, "Score": score, "Sentiment": sentiment})
df_top = pd.DataFrame(top_movers)

# Layout
col1, col2 = st.columns([1, 1])
col1.subheader("📈 Top Movers (Stocks Only)")
col1.dataframe(df_top, use_container_width=True)

col2.subheader("🌐 Indices")
st.dataframe(score_group(indices, main_tf), use_container_width=True)

st.subheader("💰 Commodities")
st.dataframe(score_group(commodities, main_tf), use_container_width=True)

st.subheader("💱 Currencies (FX + BTCUSD)")
st.dataframe(score_group(currencies, main_tf), use_container_width=True)

st.subheader("⚡ Volatility Assets")
st.dataframe(score_group(volatility, main_tf), use_container_width=True)
