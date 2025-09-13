# Yahoo Finance Scraper

## Descrição
Este projeto faz scraping de notícias financeiras do Yahoo Finance. Ele coleta títulos e links, exibe um preview no console e salva os dados em um arquivo CSV.

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


Os resultados são gravados por padrão em `dados/noticias_yahoo.csv`. Para
alterar o caminho de saída, utilize o parâmetro `--output`:

```bash
python scraper.py --output caminho/para/arquivo.csv
```


## Tecnologias Utilizadas
- Python
- Requests
- BeautifulSoup
- Pandas

## Contribuição
Contribuições são bem-vindas! Para sugerir melhorias, abra uma issue ou faça um pull request.
