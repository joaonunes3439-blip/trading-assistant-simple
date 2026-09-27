import numpy as np
import pandas as pd


def sma(series: pd.Series, window: int) -> pd.Series:
    return series.rolling(window=window, min_periods=window).mean()


def ema(series: pd.Series, span: int) -> pd.Series:
    return series.ewm(span=span, adjust=False).mean()


def rsi(series: pd.Series, period: int = 14) -> pd.Series:
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(window=period, min_periods=period).mean()
    avg_loss = loss.rolling(window=period, min_periods=period).mean()

    rs = avg_gain / avg_loss.replace(0, np.nan)
    computed = 100 - (100 / (1 + rs))
    return computed.fillna(50)


def add_indicators(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    if "Close" not in df.columns:
        raise ValueError("O DataFrame precisa ter coluna 'Close'.")

    df["SMA_20"] = sma(df["Close"], 20)
    df["SMA_50"] = sma(df["Close"], 50)
    df["EMA_9"] = ema(df["Close"], 9)
    df["EMA_21"] = ema(df["Close"], 21)
    df["RSI_14"] = rsi(df["Close"], 14)

    return df
