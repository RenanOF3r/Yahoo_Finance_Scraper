"""Scraper de notícias do Yahoo Finance.

Este módulo fornece a função ``scrape_news`` que coleta as últimas
manchetes do Yahoo Finance e retorna um ``pandas.DataFrame`` com os
resultados. Quando executado como script, o usuário pode ajustar a URL e o
número máximo de tentativas de requisição via argumentos de linha de comando.
"""

import os
import time
from urllib.parse import urljoin, urlparse

import pandas as pd
import requests
from bs4 import BeautifulSoup

# URL do Yahoo Finance para notícias
BASE_URL = "https://finance.yahoo.com"
URL = urljoin(BASE_URL, "news/")
HEADERS = {"User-Agent": "Mozilla/5.0"}  # Evita bloqueios

# Tentativa de conexão com retries
MAX_RETRIES = 3


def scrape_news(url: str = URL, max_retries: int = MAX_RETRIES) -> pd.DataFrame | None:
    """Obtém notícias do Yahoo Finance.

    Parameters
    ----------
    url : str, optional
        URL alvo, por padrão ``URL``.
    max_retries : int, optional
        Número máximo de tentativas, por padrão ``MAX_RETRIES``.

    Returns
    -------
    pandas.DataFrame | None
        DataFrame com título e link das notícias ou ``None`` em caso de erro.
    """

    response = None
    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=HEADERS, timeout=10)
            response.raise_for_status()  # Lança erro para respostas HTTP inválidas
            break  # Sai do loop se a requisição for bem-sucedida
        except requests.exceptions.RequestException as e:
            print(f"Tentativa {attempt + 1} falhou: {e}")
            time.sleep(3)  # Espera antes de tentar novamente
    else:
        print("Erro ao acessar Yahoo Finance após várias tentativas.")
        return None

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
        return pd.DataFrame(news_data)

    print("Erro ao acessar Yahoo Finance ou resposta inválida.")
    return None


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Scraper de notícias do Yahoo Finance")
    parser.add_argument("--url", default=URL, help="URL para buscar notícias")
    parser.add_argument(
        "--max_retries", type=int, default=MAX_RETRIES, help="Número máximo de tentativas"
    )
    parser.add_argument(
        "--output",
        default="dados/noticias_yahoo.csv",
        help="Caminho para salvar o CSV de saída",
    )
    args = parser.parse_args()

    df = scrape_news(url=args.url, max_retries=args.max_retries)
    if df is not None:
        # Garante que o diretório exista antes de salvar
        os.makedirs(os.path.dirname(args.output), exist_ok=True)
        df.to_csv(args.output, index=False)

        try:
            import ace_tools as tools

            tools.display_dataframe_to_user(name="Notícias Yahoo Finance", dataframe=df)
        except ModuleNotFoundError:
            # Exibe as primeiras linhas se a ferramenta não estiver disponível
            print(df.head())
    else:
        print("Erro ao acessar Yahoo Finance ou resposta inválida.")

