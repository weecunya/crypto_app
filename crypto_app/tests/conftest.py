

import pytest
import httpx

import os
from dotenv import load_dotenv



# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('register/', register, name='register'),
#     path('', include('django.contrib.auth.urls')),
#     path('profile/', profile, name='profile'),
#     path('crypto-history/',crypto_history, name='crypto_history'),
#     path('chart/', chart, name='chart'),
#     path('api-history/', api_btc_history, name='api'),
# ]

load_dotenv()

@pytest.fixture(scope="module")
def client():
    client = httpx.Client(base_url=os.environ.get("BASE_URL"))
    yield client
    client.close()

