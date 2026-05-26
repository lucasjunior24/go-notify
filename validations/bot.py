import requests
import pandas as pd

# Configuração
coin = "bitcoin"
vs_currency = "usd"
days = 30

# Buscar dados históricos
url = f"https://api.coingecko.com/api/v3/coins/{coin}/market_chart"
params = {"vs_currency": vs_currency, "days": days}

response = requests.get(url, params=params)
data = response.json()
# Converter para DataFrame

print()
prices = data["prices"]
df = pd.DataFrame(prices, columns=["timestamp", "price"])

# Converter timestamp
df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")

# Calcular médias móveis
df["SMA_7"] = df["price"].rolling(window=7).mean()
df["SMA_14"] = df["price"].rolling(window=14).mean()

# Últimos dados
latest = df.iloc[-1]

print("Preço atual:", latest["price"])
print("SMA 7:", latest["SMA_7"])
print("SMA 14:", latest["SMA_14"])

# Análise simples
if latest["price"] > latest["SMA_7"]:
    print("📈 Tendência de curto prazo: ALTA")
else:
    print("📉 Tendência de curto prazo: BAIXA")

if latest["SMA_7"] > latest["SMA_14"]:
    print("🔥 Possível sinal de alta (golden cross)")
else:
    print("⚠️ Possível sinal de baixa (death cross)")


print("\nConsultando preços atuais de várias criptomoedas...")
print("===============================================")


def get_all():

    # URL da rota simple/price para obter o valor atual
    url = "https://api.coingecko.com/api/v3/simple/price"
    # Parâmetros: ids das moedas e a moeda de conversão (vs_currencies)
    main_10_crypto_ids = [
    "bitcoin",
    "ethereum",
    "tether",
    "bnb",
    "solana",
    "ripple",
    "usd-coin",
    "cardano",
    "dogecoin",
    "tron"
]
    parametros = {"ids": ",".join(main_10_crypto_ids), "vs_currencies": "usd,brl"}

    try:
        response = requests.get(url, params=parametros)
        data = response.json()
        print(data)

        # Exibindo os valores formatados
        for moeda, valores in data.items():
            print(f"--- {moeda.upper()} ---")
            print(f"Preço em USD: ${valores['usd']:,}")
            print(f"Preço em BRL: R${valores['brl']:,}")

    except Exception as e:
        print(f"Erro ao consultar a API: {e}")


get_all()
