import random
import io
import asyncio
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

from fastapi import FastAPI
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

FOREX_PAIRS = [
"AUD/CAD","CHF/JPY","EUR/CHF","EUR/GBP","EUR/JPY",
"AUD/NZD","AUD/USD","EUR/USD","GBP/USD","USD/JPY",
"EUR/AUD","GBP/JPY","GBP/CHF","NZD/USD","USD/CAD",
"EUR/CAD","AUD/CHF","GBP/AUD","AUD/JPY","CAD/JPY"
]

OTC_PAIRS = [
"AUD/CAD OTC","CHF/JPY OTC","EUR/CHF OTC","EUR/GBP OTC",
"EUR/JPY OTC","USD/BRL OTC","USD/CHF OTC","USD/INR OTC",
"USD/SGD OTC","EUR/HUF OTC","USD/VND OTC","GBP/JPY OTC",
"NZD/USD OTC","USD/MYR OTC","USD/CNH OTC"
]

TIMEFRAMES = ["30s","1m","2m","3m","5m","10m"]

app.mount("/web", StaticFiles(directory="web"), name="web")

async def get_data(pair):
    symbol = pair.replace(" OTC","").replace("/","") + "=X"
    df = await asyncio.to_thread(
        yf.download,
        symbol,
        period="1d",
        interval="1m",
        progress=False
    )
    if df is None or len(df) < 50:
        return None
    return df

def analyze(df):
    last = df["Close"].iloc[-1]
    prev = df["Close"].iloc[-2]
    direction = "BUY" if last > prev else "SELL"
    probability = random.randint(65, 90)
    return direction, probability

@app.get("/pairs")
async def pairs():
    return {"forex": FOREX_PAIRS, "otc": OTC_PAIRS}

@app.get("/timeframes")
async def timeframes():
    return TIMEFRAMES

@app.get("/signal")
async def signal(pair: str):

    df = await get_data(pair)

    if df is None:
        return JSONResponse({"error": "No data"}, status_code=400)

    direction, prob = analyze(df)

    return {
        "pair": pair,
        "direction": direction,
        "probability": prob
    }

@app.get("/chart")
async def chart(pair: str):

    df = await get_data(pair)

    if df is None:
        return JSONResponse({"error":"No data"}, status_code=400)

    plt.figure()
    df["Close"].tail(50).plot()
    plt.title(pair)
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    plt.close()

    return StreamingResponse(buf, media_type="image/png")