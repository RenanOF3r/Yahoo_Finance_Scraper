import pandas as pd
from unittest.mock import Mock, patch
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))
from scraper import scrape_news, NEWS_HEADLINE_SELECTOR

SAMPLE_HTML = '''
<ul>
  <li class="js-stream-content">
    <h3 class="Mb(5px)"><a href="/news/foo">Foo</a></h3>
  </li>
  <li class="js-stream-content">
    <h3 class="Mb(5px)"><a href="/news/bar">Bar</a></h3>
  </li>
  <li>
    <h3><a href="/other">Other</a></h3>
  </li>
</ul>
'''

def test_scrape_news_uses_specific_selector():
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.text = SAMPLE_HTML
    mock_response.raise_for_status = Mock()
    with patch('requests.get', return_value=mock_response):
        df = scrape_news(url='http://test', max_retries=1)
    assert isinstance(df, pd.DataFrame)
    assert df['Título'].tolist() == ['Foo', 'Bar']
    assert df['Link'].tolist() == [
        'https://finance.yahoo.com/news/foo',
        'https://finance.yahoo.com/news/bar'
    ]
