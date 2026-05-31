
import requests
from celery import shared_task
from crypto_app.models import CryptoPrice


@shared_task
def fetch_client():
    symbols = ['BTCUSDT', 'ETHUSDT', 'SOLUSDT', 'XRPUSDT', 'DOGEUSDT']
    for symbol in symbols:
        try:
            response = requests.get(f"https://api.binance.com/api/v3/ticker/24hr?symbol={symbol}")
            price = response.json()["lastPrice"]
            CryptoPrice.objects.create(symbol=symbol, price=price)
        except Exception as e:
            print(e)
    return f"saved prices for {len(symbols)} symbols"
    # print(response.json())
    # print(price)

# def api_client():
#     response = requests.get(f"https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1h&limit=5")
#     return response
