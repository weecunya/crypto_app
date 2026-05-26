from app.config import settings
from aiohttp import ClientSession

class APIClient:
    @staticmethod
    async def get_weather(city:str):
        async with ClientSession() as session:
            try:
                async with session.get(f'https://www.meteoblue.com/en/server/search/query3?query={city}&api_key={settings.API_KEY}') as resp:
                    data = await resp.json()
                    lat,lon = data['results'][0]['lat'], data['results'][0]['lon']
                    # print(lat,lon)

                async with session.get(f'https://my.meteoblue.com/packages/basic-1h_basic-day?apikey={settings.API_KEY}&lat={lat}&lon={lon}&asl=222&format=json') as response:
                    result = await response.json()
                    # print(result)

                    return {
        f'{city}': {f'''{result['data_day']['time'][0]}: макс.темп.- {result['data_day']['temperature_max'][0]},
мин.темп.- {result['data_day']['temperature_min'][0]}, вероятность осадков-{result['data_day']['precipitation_probability'][0]}%'''}}

            except Exception:
                return {'status': 'not found'}


#


client = APIClient()