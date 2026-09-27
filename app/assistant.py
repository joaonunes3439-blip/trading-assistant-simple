from typing import Dict

from app.data import fetch_market_data
from app.indicators import add_indicators


class SimpleTradingAssistant:
    def __init__(self, asset: str, market: str):
        self.asset = asset.strip().upper()
        self.market = market.strip().lower()
        self.df = add_indicators(fetch_market_data(self.asset, self.market))

    def get_summary(self) -> Dict[str, str]:
        last = self.df.iloc[-1]
        previous = self.df.iloc[-2]
        close = float(last["Close"])
        prev_close = float(previous["Close"])
        change = ((close - prev_close) / prev_close) * 100

        sma_20 = float(last["SMA_20"])
        sma_50 = float(last["SMA_50"])
        ema_9 = float(last["EMA_9"])
        ema_21 = float(last["EMA_21"])
        rsi = float(last["RSI_14"])

        if close > sma_20 > sma_50:
            trend = "alta estruturada"
        elif close < sma_20 < sma_50:
            trend = "baixa estruturada"
        else:
            trend = "tendência neutra/indefinida"

        if rsi > 70:
            momentum = "sobrecompra"
        elif rsi < 30:
            momentum = "oversold"
        else:
            momentum = "equilibrado"

        if ema_9 > ema_21:
            alignment = "EMA curta acima da longa"
        else:
            alignment = "EMA curta abaixo da longa"

        if change > 0:
            direction = "positivo"
        else:
            direction = "negativo"

        risk_level = "médio" if 35 <= rsi <= 65 else "alto"
        entry = "registrar confirmação de compra" if trend == "alta estruturada" else "aguardar confirmação"
        exit_signal = "vender ou reduzir se a estrutura enfraquecer" if trend != "alta estruturada" else "proteger lucro se perder média"

        return {
            "asset": self.asset,
            "market": self.market,
            "trend": trend,
            "momentum": momentum,
            "alignment": alignment,
            "direction": direction,
            "change_pct": round(change, 2),
            "rsi": round(rsi, 2),
            "price": round(close, 2),
            "risk_level": risk_level,
            "entry": entry,
            "exit_signal": exit_signal,
            "summary": (
                f"{self.asset} está em {trend} com movimento {direction} e RSI em {round(rsi, 2)} "
                f"({momentum}). A estrutura de médias está em {alignment}. "
                f"O preço atual está em R$ {round(close, 2)} e a variação do último candle foi {round(change, 2)}%. "
                f"A recomendação prática é: {entry}."
            ),
        }
