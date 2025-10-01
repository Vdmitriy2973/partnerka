import aiohttp

async def fetch_bank_data(query: str):
    url = f"https://bins.antipublic.cc/bins/{query}"
    if len(query) < 6:
        return None
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                url,
                timeout=5  # Таймаут 5 секунд
            ) as response:
                response.raise_for_status()  # Проверка на ошибки HTTP
                data = await response.json()
                print(data["bank"])
                return data["bank"]
                
    except aiohttp.ClientError as e:
        print(f"Ошибка запроса: {e}")
        return None