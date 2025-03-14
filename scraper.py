import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# URL do Yahoo Finance para notícias
URL = "https://finance.yahoo.com/news/"
HEADERS = {"User-Agent": "Mozilla/5.0"}  # Evita bloqueios

# Tentativa de conexão com retries
MAX_RETRIES = 3
for attempt in range(MAX_RETRIES):
    try:
        response = requests.get(URL, headers=HEADERS, timeout=10)
        response.raise_for_status()  # Lança erro para respostas HTTP inválidas
        break  # Sai do loop se a requisição for bem-sucedida
    except requests.exceptions.RequestException as e:
        print(f"Tentativa {attempt + 1} falhou: {e}")
        time.sleep(3)  # Espera antes de tentar novamente
else:
    print("Erro ao acessar Yahoo Finance após várias tentativas.")
    response = None

if response and response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")

    # Encontrando os blocos de notícia
    articles = soup.find_all("h3")  # Yahoo usa <h3> para manchetes

    news_data = []
    for article in articles:
        title = article.text
        link = "https://finance.yahoo.com" + article.a["href"] if article.a else "N/A"
        news_data.append({"Título": title, "Link": link})

    # Criar DataFrame
    df = pd.DataFrame(news_data)

    # Exibir as primeiras notícias
    import ace_tools as tools
    tools.display_dataframe_to_user(name="Notícias Yahoo Finance", dataframe=df)
else:
    print("Erro ao acessar Yahoo Finance ou resposta inválida.")
