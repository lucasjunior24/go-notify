import os
from dotenv import load_dotenv

# encoding: utf-8
load_dotenv()
from efipay import EfiPay

CLIENT_ID = os.getenv("PROD_CLIENT_ID")
CLIENT_SECRET = os.getenv("PROD_CLIENT_SECRET")
CERTIFICATE_PATH = os.getenv("PROD_CERTIFICATE_PATH")

PROD_CHAVE_PIX = os.getenv("PROD_CHAVE_PIX")

# PRODUÇÃO = false
# HOMOLOGAÇÃO = true
credentials = {
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET,
    "sandbox": False,
    "certificate": CERTIFICATE_PATH,
}
print(credentials)
print()
efi = EfiPay(credentials)

body = {
    "calendario": {"expiracao": 3600},
    "devedor": {"cpf": "12345678909", "nome": "Francisco da Silva"},
    "valor": {"original": "0.45"},
    "chave": PROD_CHAVE_PIX,
    "solicitacaoPagador": "Cobrança dos serviços prestados.",
}

response = efi.pix_create_immediate_charge(body=body)
print(response)
print()
print(response["pixCopiaECola"])
