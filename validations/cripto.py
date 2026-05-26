import requests

url = "https://api.coingecko.com/api/v3/simple/price"

params = {
    "ids": "bitcoin",
    "vs_currencies": "usd,brl"
}

response = requests.get(url, params=params)

if response.status_code == 200:
    data = response.json()
    print("Preço do Bitcoin:")
    in_dollars = data['bitcoin']['usd']
    in_reais = data['bitcoin']['brl']
    print(f"USD: {float(in_dollars):.2f}")
    print(f"BRL: {float(in_reais):.2f}")
else:
    print("Erro na requisição:", response.status_code)