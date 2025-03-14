# Yahoo Finance Scraper

## Descrição
Este projeto faz scraping de notícias financeiras do Yahoo Finance. Ele coleta títulos, links e exibe os dados em um DataFrame.

## Instalação
1. Clone este repositório:
   ```bash
   git clone https://github.com/seuusuario/yahoo-finance-scraper.git
   cd yahoo-finance-scraper
   ```

2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

## Uso
Execute o script para coletar as últimas notícias:
```bash
python scraper.py
```

O script tentará conectar até 3 vezes caso haja falhas na requisição.

## Tecnologias Utilizadas
- Python
- Requests
- BeautifulSoup
- Pandas

## Contribuição
Contribuições são bem-vindas! Para sugerir melhorias, abra uma issue ou faça um pull request.
