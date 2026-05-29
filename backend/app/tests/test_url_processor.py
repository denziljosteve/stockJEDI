from app.services.url_processor import URLProcessor

def test_process_yahoo_url():
    url = "https://finance.yahoo.com/quote/AAPL"
    ticker, source = URLProcessor.process_url(url)
    assert ticker == "AAPL"
    assert source == "Yahoo Finance"

def test_process_screener_url():
    url = "https://www.screener.in/company/RELIANCE/"
    ticker, source = URLProcessor.process_url(url)
    assert ticker == "RELIANCE"
    assert source == "Screener.in"

def test_validate_ticker():
    assert URLProcessor.validate_ticker("AAPL") is True
    assert URLProcessor.validate_ticker("RELIANCE") is True
    assert URLProcessor.validate_ticker("VERYLONGTICKER") is False
    assert URLProcessor.validate_ticker("") is False
