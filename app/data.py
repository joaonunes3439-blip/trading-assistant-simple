import os
from typing import Dict, List

import pandas as pd
import yfinance as yf
import ccxt


def fetch_stock_data(symbol: str, period: str = "1y", interval: str = "1d") -> pd.DataFrame:
    df = yf.download(symbol, period=period, interval=interval, auto_adjust=True, progress=False)
    if df.empty:
        raise ValueError(f"Nenhum dado encontrado para {symbol}.")

    df = df.reset_index()
    df.columns = [str(column).strip() for column in df.columns]

    if "Date" not in df.columns:
        if "Datetime" in df.columns:
            df = df.rename(columns={"Datetime": "Date"})
        else:
            df["Date"] = pd.to_datetime(df.index)

    df["Date"] = pd.to_datetime(df["Date"])
    columns = ["Date", "Open", "High", "Low", "Close", "Volume"]
    return df[[column for column in columns if column in df.columns]].copy()


def fetch_crypto_data(symbol: str, timeframe: str = "1d", limit: int = 365) -> pd.DataFrame:
    exchange = ccxt.binance()
    pair = f"{symbol.upper()}/USDT"
    ohlcv = exchange.fetch_ohlcv(pair, timeframe=timeframe, limit=limit)

    if not ohlcv:
        raise ValueError(f"Nenhum dado encontrado para {pair}.")

    df = pd.DataFrame(ohlcv, columns=["Timestamp", "Open", "High", "Low", "Close", "Volume"])
    df["Date"] = pd.to_datetime(df["Timestamp"], unit="ms")
    return df[["Date", "Open", "High", "Low", "Close", "Volume"]].copy()


def fetch_market_data(asset: str, market: str) -> pd.DataFrame:
    asset = asset.strip().upper()
    market = market.strip().lower()

    if market == "stock":
        return fetch_stock_data(asset)
    if market == "crypto":
        return fetch_crypto_data(asset)
    raise ValueError(" Mercado inválido. Use 'stock' ou 'crypto'.")
