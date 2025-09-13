import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from urllib.parse import urljoin, urlparse

# URL do Yahoo Finance para notícias
BASE_URL = "https://finance.yahoo.com"
URL = urljoin(BASE_URL, "news/")
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
        href = article.a.get("href") if article.a else ""
        if href:
            full_url = urljoin(BASE_URL, href)
            parsed = urlparse(full_url)
            link = full_url if parsed.scheme and parsed.netloc else "N/A"
        else:
            link = "N/A"
        news_data.append({"Título": title, "Link": link})

    # Criar DataFrame
    df = pd.DataFrame(news_data)

    # Exibir as primeiras notícias
    import ace_tools as tools
    tools.display_dataframe_to_user(name="Notícias Yahoo Finance", dataframe=df)
else:
    print("Erro ao acessar Yahoo Finance ou resposta inválida.")
