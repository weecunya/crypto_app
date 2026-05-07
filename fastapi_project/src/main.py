
import fastapi
from src.http_client import client

app = fastapi.FastAPI()
cash_dict = {}

@app.get('/')
def home_page():
    return {'status': 'ok'}

@app.get("/{city_name}")
async def give_weather(city_name:str):
    try:
        if not city_name in cash_dict.keys():
            response = await client.get_weather(city_name)
            cash_dict[city_name] = response
            return {'result': response}
        else:
            response = cash_dict[city_name]
            return {'result': response}
    finally:
        if len(cash_dict.keys()) > 5:
            cash_dict.clear()
        print(len(cash_dict.keys()))



