import os
from dotenv import load_dotenv

load_dotenv()


USER_DB_KEY = os.getenv("USER_DB")

if USER_DB_KEY:
    print("Chave de API carregada com sucesso:", USER_DB_KEY)
else:
    print("Chave de API não encontrada no arquivo .env")

APP_NAME_KEY = os.getenv("APP_NAME")
PASSWORD_DB_KEY = os.getenv("PASSWORD_DB")

DB_NAME = os.getenv("DB_NAME", "notify")
IP_WITH_PORT_DB = os.getenv("IP_WITH_PORT_DB")
CHAT_API_URL = os.getenv("CHAT_API_URL")
DB_URL = f"mongodb://{IP_WITH_PORT_DB}"
# NEW_DB_URL = f"mongodb+srv://{USER_DB_KEY}:{PASSWORD_DB_KEY}@{DB_URL}/?retryWrites=true&w=majority&appName={APP_NAME_KEY}"
# NEW_DB_URL = os.getenv("NEW_DB_URL")

print(DB_NAME)
print(DB_URL)
