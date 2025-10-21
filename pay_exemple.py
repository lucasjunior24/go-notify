import os
from dotenv import load_dotenv

# encoding: utf-8
load_dotenv()
from efipay import EfiPay

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
CERTIFICATE_PATH = os.getenv("CERTIFICATE_PATH")


# PRODUÇÃO = false
# HOMOLOGAÇÃO = true
credentials = {
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET,
    "sandbox": True,
    "certificate": CERTIFICATE_PATH,
}
print(credentials)
print()
efi = EfiPay(credentials)

body = {
    "calendario": {"expiracao": 3600},
    "devedor": {"cpf": "12345678909", "nome": "Francisco da Silva"},
    "valor": {"original": "0.45"},
    "chave": "71cdf9ba-c695-4e3c-b010-abb521a3f1be",
    "solicitacaoPagador": "Cobrança dos serviços prestados.",
}

response = efi.pix_create_immediate_charge(body=body)
print(response)
print()
print(response["pixCopiaECola"])
