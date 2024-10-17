# # # # # # # # # # # # 
# # nomi_client.py # # 
# # # # # # # # # # # # 
import aiohttp
import asyncio
import json

class NomiClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.nomi.ai/v1"
        self.headers = {
            "Authorization": self.api_key,
            "Content-Type": "application/json",
        }
        self.introduction_message = (
            "Hi Nomi pal! Just so you know, I have a special device that responds when you use words like "
            "\"vibrate\", \"buzz\", \"pulse\", or \"shake\" followed by a number between 1 and 20. "
            "You can also tell it to \"stop\" or use the patterns \"pulse\", \"wave\", \"fireworks\", "
            "or \"earthquake\". Feel free to have fun with it!"
        )

    async def list_nomis(self):
        url = f"{self.base_url}/nomis"
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self.headers) as response:
                content_type = response.content_type
                if content_type == "application/json":
                    data = await response.json()
                else:
                    data = json.loads(await response.text())
                return data

    async def get_nomi(self, nomi_id):
        url = f"{self.base_url}/nomis/{nomi_id}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self.headers) as response:
                data = await response.json()
                return data

    async def send_message(self, nomi_id, message_text):
        url = f"{self.base_url}/nomis/{nomi_id}/chat"
        payload = {"messageText": message_text}
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, headers=self.headers) as response:
                data = await response.json()
                return data
