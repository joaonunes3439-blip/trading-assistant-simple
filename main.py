import os
from contextlib import suppress

from dotenv import load_dotenv

load_dotenv()


def try_ollama_summary(asset: str, market: str, analysis: dict) -> str | None:
    try:
        import ollama
    except Exception:
        return None

    model = os.getenv("OLLAMA_MODEL", "llama3.1")
    prompt = (
        f"Você é um analista de mercado para trading. Responda em português e seja objetivo. "
        f"Ativo: {asset}. Mercado: {market}. "
        f"Resumo técnico: tendência={analysis['trend']}, RSI={analysis['rsi']}, risco={analysis['risk_level']}, "
        f"preço={analysis['price']}, variação={analysis['change_pct']}%. "
        f"Dê um resumo prático com 5 itens: tendência, risco, setup, entrada e saída."
    )

    with suppress(Exception):
        response = ollama.chat(
            model=model,
            messages=[
                {"role": "system", "content": "Você é um analista para trading. Responda em português."},
                {"role": "user", "content": prompt},
            ],
        )
        return response["message"]["content"]

    return None


def try_openai_summary(asset: str, market: str, analysis: dict) -> str | None:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return None

    try:
        from openai import OpenAI
    except Exception:
        return None

    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    client = OpenAI(api_key=api_key)

    prompt = (
        f"Analise este cenário de trading em português: "
        f"ativo={asset}, mercado={market}, tendência={analysis['trend']}, rsi={analysis['rsi']}, risco={analysis['risk_level']}, "
        f"preço={analysis['price']}, variação={analysis['change_pct']}%. "
        "Responda em 5 pontos: tendência, risco, setup, entrada e saída."
    )

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "Você é um analista de mercado auxiliares para trading."},
                {"role": "user", "content": prompt},
            ],
        )
        return response.choices[0].message.content
    except Exception:
        return None


def get_summary_from_ai(asset: str, market: str, analysis: dict) -> str:
    ai_summary = try_ollama_summary(asset, market, analysis)
    if ai_summary:
        return ai_summary

    ai_summary = try_openai_summary(asset, market, analysis)
    if ai_summary:
        return ai_summary

    return analysis["summary"]
