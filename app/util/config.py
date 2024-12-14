import os
from dotenv import load_dotenv

load_dotenv()


USER_DB_KEY = os.getenv("USER_DB")

if USER_DB_KEY:
    print("Chave de API carregada com sucesso:", USER_DB_KEY)
else:
    print("Chave de API não encontrada no arquivo .env")


PASSWORD_DB_KEY = os.getenv("PASSWORD_DB")
DB_NAME_KEY = os.getenv("DB_NAME")
APP_NAME_KEY = os.getenv("APP_NAME")
IP = os.getenv("IP", "172.17.48.1:27017")
# DB_URL = f"mongodb+srv://{USER_DB_KEY}:{PASSWORD_DB_KEY}@{DB_NAME_KEY}/?retryWrites=true&w=majority&appName={APP_NAME_KEY}"
# DB_URL = os.getenv("DB_URL")
DB_URL = f"mongodb://{IP}"

print(DB_NAME_KEY)
print(DB_URL)