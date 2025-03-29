from efipay import EfiPay

credentials = {
    "client_id": "client_id",
    "client_secret": "client_secret",
    "sandbox": True,
    "certificate": "insira-o-caminho-completo-do-certificado",
}

efi = EfiPay(credentials)

body = {
    "calendario": {"expiracao": 3600},
    "devedor": {"cpf": "12345678909", "nome": "Francisco da Silva"},
    "valor": {"original": "123.45"},
    "chave": "71cdf9ba-c695-4e3c-b010-abb521a3f1be",
    "solicitacaoPagador": "Cobrança dos serviços prestados.",
}

response = efi.pix_create_immediate_charge(body=body)
print(response)
