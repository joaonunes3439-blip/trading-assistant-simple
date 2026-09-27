# Trading Assistant Simple

Um assistente pessoal de análise para ações e cripto, pensado como MVP simples para rodar no seu PC.

O projeto busca dados do mercado, calcula indicadores básicos, interpreta o cenário com lógica de análise técnica e, se configurado, usa IA local (Ollama) ou API OpenAI para resumir o contexto.

## Funcionalidades
- Busca de dados de ações com Yahoo Finance
- Busca de dados de cripto com Binance via CCXT
- Indicadores básicos:
  - SMA 20
  - SMA 50
  - EMA 9
  - EMA 21
  - RSI 14
- Resumo textual do momento do mercado
- CLI simples para testar rapidamente
- Estrutura pronta para evoluir com dashboard, alertas e watchlist

## Estrutura

```text
trading-assistant-simple/
├── app/
│   ├── __init__.py
│   ├── assistant.py
│   ├── data.py
│   └── indicators.py
├── .env.example
├── .gitignore
├── main.py
├── README.md
├── requirements.txt
└── venv/
```

## Instalação

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
# ou venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

## Configuração opcional de IA

Copie o arquivo de exemplo:

```bash
cp .env.example .env
```

Editar `.env` e configurar um modelo se quiser usar IA no resumo:

```env
OLLAMA_MODEL=llama3.1
OPENAI_MODEL=gpt-4o-mini
OPENAI_API_KEY=
```

## Como usar

```bash
python main.py
```

Você será solicitado a informar:
- ativo (ex.: AAPL, BTC)
- mercado (stock ou crypto)

Exemplo:

```text
Digite o ativo (ex.: AAPL, BTC): AAPL
Digite o mercado (stock ou crypto): stock
```

O programa retornará:
- tendência
- nível de risco
- indicação de entrada/saída
- stop e alvo sugeridos
- resumo do contexto com indicadores

## Observações
Este projeto é um MVP de apoio à análise e não substitui gestão de risco, disciplina e estudo de mercado. Não é recomendação financeira.

## Próximos passos sugeridos
- Dashboard com Streamlit
- Watchlist
- Alertas por Telegram
- Suporte a múltiplos ativos
- Registro de carteira
- Backtesting simples
- IA mais avançada com memória e contexto

