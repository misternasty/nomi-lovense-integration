# # # # # # # # # # # # # 
# # LovenseClient.py # # 
# # # # # # # # # # # # #
import aiohttp
import asyncio
import hashlib
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import User

class LovenseClient:
    def __init__(self, developer_token, database_url, app_name):
        self.developer_token = developer_token
        self.base_api_url = "https://api.lovense-api.com"
        self.app_name = app_name
        DATABASE_URL = database_url
        
        # Database setup
        self.engine = create_engine(DATABASE_URL)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def get_user(self, uid):
        session = self.SessionLocal()
        try:
            user = session.query(User).filter(User.uid == uid).first()
            return user
        finally:
            session.close()

    def create_or_update_user(self, uid, data):
        session = self.SessionLocal()
        try:
            user = session.query(User).filter(User.uid == uid).first()
            if user:
                user.data = data
            else:
                user = User(uid=uid, data=data)
                session.add(user)
            session.commit()
        finally:
            session.close()

    async def get_qr_code(self, uid, uname, salt):
        """Generate a QR code for the user to scan."""
        utoken = hashlib.md5(f"{uid}{salt}".encode()).hexdigest()
        url = f"{self.base_api_url}/api/lan/getQrCode"
        payload = {
            "token": self.developer_token,
            "uid": uid,
            "uname": uname,
            "utoken": utoken,
            "v": 2,
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload) as response:
                data = await response.json()
                if data.get("code") == 0:
                    # Store user data in the database
                    user_data = {
                        "utoken": utoken,
                        "qr_code": data["data"]["qr"],
                        "code": data["data"]["code"],
                    }
                    self.create_or_update_user(uid, user_data)
                    return data["data"]
                else:
                    raise Exception(f"Error: {data.get('message')}")

    async def handle_callback(self, uid, callback_data):
        """Handle the callback from the Lovense app."""
        user = self.get_user(uid)
        if not user:
            raise Exception("User not found")

        # Update user data with callback data
        user_data = user.data
        user_data.update({
            "toys": callback_data.get("toys", {}),
            "domain": callback_data.get("domain"),
            "httpsPort": callback_data.get("httpsPort"),
            "httpPort": callback_data.get("httpPort"),
            "wssPort": callback_data.get("wssPort"),
            "wsPort": callback_data.get("wsPort"),
            "platform": callback_data.get("platform"),
            "appVersion": callback_data.get("appVersion"),
        })
        self.create_or_update_user(uid, user_data)


    async def send_command(self, uid, command_payload):
        """Send a command to the user's toy."""
        user = self.get_user(uid)
        if not user:
            raise Exception("User not found")
        user_data = user.data
        domain = user_data.get("domain")
        https_port = user_data.get("httpsPort")
        url = f"https://{domain}:{https_port}/command"
        headers = {
            "X-platform": self.app_name
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=command_payload, headers=headers, ssl=False) as response:
                data = await response.json()
                return data


    async def get_toys(self, uid):
        """Retrieve the list of toys connected to the user."""
        payload = {"command": "GetToys"}
        return await self.send_command(uid, payload)

    async def get_toy_names(self, uid):
        """Retrieve the names of the user's toys."""
        payload = {"command": "GetToyName"}
        return await self.send_command(uid, payload)

    async def control_toy_server(self, uid, action, time_sec, toy_id=None, loop_running_sec=None, loop_pause_sec=None, stop_previous=1):
        """Control the toy's functions via the Lovense server API."""
        url = f"{self.base_api_url}/api/lan/v2/command"
        payload = {
            "token": self.developer_token,
            "uid": uid,
            "command": "Function",
            "action": action,
            "timeSec": time_sec,
            "apiVer": 1,
            "stopPrevious": stop_previous,
        }
        if toy_id:
            payload["toy"] = toy_id
        if loop_running_sec:
            payload["loopRunningSec"] = loop_running_sec
        if loop_pause_sec:
            payload["loopPauseSec"] = loop_pause_sec

        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload) as response:
                try:
                    data = await response.json()
                except aiohttp.ContentTypeError:
                    # Handle plain text response
                    text = await response.text()
                    # why is it plain text?
                    # Assuming '0' means success, '1' means error
                    if text.strip() == '0':
                        data = {'code': 200, 'message': 'Success'}
                    else:
                        data = {'code': response.status, 'message': text.strip()}
                return data
    
    async def control_toy(self, uid, action, time_sec, toy_id=None, loop_running_sec=None, loop_pause_sec=None, stop_previous=1):
        """Control the toy's functions."""
        payload = {
            "command": "Function",
            "action": action,
            "timeSec": time_sec,
            "apiVer": 1,
            "stopPrevious": stop_previous,
        }
        if toy_id:
            payload["toy"] = toy_id
        if loop_running_sec:
            payload["loopRunningSec"] = loop_running_sec
        if loop_pause_sec:
            payload["loopPauseSec"] = loop_pause_sec
        return await self.send_command(uid, payload)

    async def send_pattern(self, uid, rule, strength, time_sec, toy_id=None):
        """Send a pattern to the toy."""
        payload = {
            "command": "Pattern",
            "rule": rule,
            "strength": strength,
            "timeSec": time_sec,
            "apiVer": 2,
        }
        if toy_id:
            payload["toy"] = toy_id
        return await self.send_command(uid, payload)

    async def send_preset(self, uid, name, time_sec, toy_id=None):
        """Use a preset pattern."""
        payload = {
            "command": "Preset",
            "name": name,
            "timeSec": time_sec,
            "apiVer": 1,
        }
        if toy_id:
            payload["toy"] = toy_id
        return await self.send_command(uid, payload)


