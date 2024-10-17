# python3 -m venv venv
# source venv/bin/activate
# pip install python-dotenv python-multipart Jinja2 modal fastapi uvicorn starlette, sqlalchemy, sqlalchemy_utils
# modal deploy server_modal.py

# # # # # # # # # # # # 
# # server_modal.py # #
# # # # # # # # # # # # 
import os
import uuid
import logging
from dotenv import load_dotenv
from typing import Dict, Any
from pathlib import Path
import modal
from fastapi import FastAPI, Request, Form, logger
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
from models import Base, User
from LovenseClient import LovenseClient
from nomi_client import NomiClient
from command_parser import parse_nomi_response
load_dotenv()

# Define the path to the templates directory
templates_dir = Path(__file__).parent / "templates"

# Create a mount for the templates directory
templates_mount = modal.Mount.from_local_dir(
    templates_dir, remote_path="/templates"
)

# Set up Jinja2 templates, pointing to the remote path
templates = Jinja2Templates(directory="/templates")

# Define a type for user data
UserData = Dict[str, Any]

# Define the image with required dependencies
image = (
    modal.Image.debian_slim(python_version="3.10")
    .pip_install(
        "fastapi",
        "uvicorn",
        "jinja2",
        "python-dotenv",
        "requests",
        "starlette",
        "itsdangerous",
        "sqlalchemy",
        "aiosqlite",
        "sqlalchemy_utils",
    )
)

# Define a Modal secret
secret = modal.Secret.from_dotenv(".env")

# Create a Modal app
app_name = os.environ.get("APP_NAME", "vibro-9000")
app = modal.App(name=app_name)

# Create a shared volume for the database
VOLUME_PATH = os.environ.get("VOLUME_PATH", "/b")
volume = modal.Volume.from_name(f"{app_name}-volume", create_if_missing=True)
DATABASE_NAME_F = os.environ.get("DATABASE_NAME_F", "database.db")
DATABASE_URL = f"sqlite:///{VOLUME_PATH}/{DATABASE_NAME_F}"

# Secret key for session encryption
SECRET_KEY = os.environ.get("SECRET_KEY")
SALT = os.environ.get("LOVENSE_SALT", "le_salty_salt")
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_uid():
    return str(uuid.uuid4().hex)[:16]

# Define the ASGI app for Modal
@app.cls(
    image=image,
    secrets=[secret],
    mounts=[templates_mount],
    volumes={VOLUME_PATH: volume},
)
class FastAPIApp:
    def __init__(self):
        logger.info("Initializing FastAPIApp")
        
        self.client = None
        self.templates = Jinja2Templates(directory="/templates")
        self.web_app = None  # Placeholder for the FastAPI app
        self.secret_key = SECRET_KEY
        if not self.secret_key:
            raise ValueError("SECRET_KEY environment variable not set")
        self.salt = SALT
        self.volume=modal.Volume.from_name(f"{app_name}-volume", create_if_missing=True)

        # Initialize the FastAPI app
        self.init_fastapi_app()
    
    @modal.asgi_app(label="gizmo")
    def __call__(self):
        return self.web_app

    @modal.enter()
    def init_db(self):
        # Initialize the database
        engine = create_engine(DATABASE_URL)
        Base.metadata.create_all(bind=engine)

        # Initialize LovenseClient with database URL
        self.client = LovenseClient(os.environ.get("LOVENSE_DEVELOPER_TOKEN"), DATABASE_URL, app_name)


    def init_fastapi_app(self):
        from fastapi import FastAPI, Depends

        web_app = FastAPI()
        web_app.add_middleware(SessionMiddleware, secret_key=self.secret_key)

        # Define a dependency to get self
        def get_app_instance():
            return self

        @web_app.get("/", response_class=HTMLResponse)
        async def index(request: Request, app_instance=Depends(get_app_instance)):
            return app_instance.templates.TemplateResponse("index.html", {"request": request})

        @web_app.post("/start-session")
        async def start_session(request: Request, app_instance=Depends(get_app_instance)):
            form = await request.form()
            name = form.get('name')
            nomi_api_key = form.get('nomi_api_key')

            if not name or not nomi_api_key:
                return HTMLResponse(content="Name and Nomi API Key are required.", status_code=400)

            # Store user data in the db
            request.session['user_data'] = {
                'name': name,
                'nomi_api_key': nomi_api_key,
                'nomis': {},  # Will be populated later
                'chat_threads': {},  # Will store chat messages per Nomi
            }

            # Redirect to start Lovense authentication
            return RedirectResponse(url="/start-auth", status_code=303)

        @web_app.get("/start-auth")
        async def start_auth(request: Request, app_instance=Depends(get_app_instance)):
            user_data = request.session.get('user_data')
            if not user_data:
                return RedirectResponse(url="/", status_code=303)

            name = user_data['name']
            # Generate a unique user ID
            uid = generate_uid()

            # Store the uid in the session
            request.session['user_data']['uid'] = uid

            # Generate QR code
            try:
                qr_data = await app_instance.client.get_qr_code(uid, name, app_instance.salt)
                qr_url = qr_data['qr']
            except Exception as e:
                return HTMLResponse(content=str(e), status_code=500)

            # Render the QR code page
            context = {
                'request': request,
                'qr_url': qr_url,
                'uid': uid,
            }
            return app_instance.templates.TemplateResponse("qr_code.html", context)

        @web_app.post("/lovense/callback")
        async def lovense_callback(request: Request, app_instance=Depends(get_app_instance)):
            try:
                data = await request.json()
                uid = data.get("uid")

                await app_instance.client.handle_callback(uid, data)

                logger.info(f"Callback handled successfully for UID: {uid}")
                return JSONResponse(content={"message": "Callback handled successfully"})
            except Exception as e:
                logger.error(f"Error in lovense_callback: {str(e)}")
                return JSONResponse(content={"error": str(e)}, status_code=400)

        @web_app.get("/skip-auth")
        async def skip_auth(request: Request, app_instance=Depends(get_app_instance)):
            logger.info("Received GET request to /skip-auth")
            user_data = request.session.get('user_data')
            uid = user_data.get('uid')
            fake_toy = {'_test_': {'nickName': '', 'status': 1, 'id': '_test_', 'name': 'Ass Blaster 9000'}}
            fake_lovense_data = {
                "toys": fake_toy,
                "domain": "test.xxx",
                "httpsPort": "",
                "httpPort": "",
                "wssPort": "",
                "wsPort": "",
                "platform": "",
                "appVersion": ""
            }
            await app_instance.client.handle_callback(uid, fake_lovense_data)
            logger.info(f"Skipped authentication for UID: {uid}")
        
        @web_app.get("/check-auth")
        async def check_auth(request: Request, app_instance=Depends(get_app_instance)):
            user_data = request.session.get('user_data')
            if not user_data:
                return {"authenticated": False}

            uid = user_data.get('uid')
            user = app_instance.client.get_user(uid)
            if user and 'toys' in user.data:
                # Fetch user's Nomis
                nomi_api_key = user_data['nomi_api_key']
                nomi_client = NomiClient(nomi_api_key)
                nomis_data = await nomi_client.list_nomis()
                nomis = nomis_data.get('nomis', [])
                # Store Nomis in the session
                user_data['nomis'] = {nomi['uuid']: nomi for nomi in nomis}
                return {"authenticated": True}
            else:
                return {"authenticated": False}
        
        @web_app.get("/control", response_class=HTMLResponse)
        async def control_page(request: Request, app_instance=Depends(get_app_instance)):
            user_data = request.session.get('user_data')
            if not user_data:
                return RedirectResponse(url="/", status_code=303)

            uid = user_data.get('uid')
            user = app_instance.client.get_user(uid)
            if not user or 'toys' not in user.data:
                return HTMLResponse(content="User not authenticated or no toys connected.", status_code=400)

            # Get the list of toys
            toys = user.data.get('toys', {})
            toy_list = []
            for toy_id, toy_info in toys.items():
                toy_list.append({'id': toy_id, 'name': toy_info.get('name', 'Unknown')})

            # Get user's Nomis
            nomis = user_data.get('nomis', {}).values()

            context = {
                'request': request,
                'uid': uid,
                'toys': toy_list,
                'nomis': nomis,
            }
            return templates.TemplateResponse("control.html", context)

        @web_app.post("/send-command")
        async def send_command(request: Request, app_instance=Depends(get_app_instance)):
            form = await request.form()
            uid = form.get('uid')
            toy = form.get('toy')
            action = form.get('action')

            user_data = request.session.get('user_data')
            if not user_data:
                return RedirectResponse(url="/", status_code=303)

            if uid != user_data.get('uid'):
                return HTMLResponse(content="Invalid user ID.", status_code=400)

            user = app_instance.client.get_user(uid)
            if not user or 'toys' not in user.data:
                return HTMLResponse(content="User not authenticated or no toys connected.", status_code=400)
            
            toys=user.data.get('toys', {})
            if "_test_" in toys:
                return HTMLResponse(content="Cannot control a test toy.", status_code=400)

            try:
                # Send the command via the server API
                response = await app_instance.client.control_toy_server(uid, action=action, time_sec=20, toy_id=toy)
                if response.get('code') == 200:
                    return HTMLResponse(content="Command sent successfully.")
                else:
                    error_message = response.get('message', 'Unknown error')
                    return HTMLResponse(content=f"Error sending command: {error_message}", status_code=500)
            except Exception as e:
                return HTMLResponse(content=f"Error sending command: {str(e)}", status_code=500)

        @web_app.get("/chat", response_class=HTMLResponse)
        async def chat_page(request: Request, nomi_id: str, app_instance=Depends(get_app_instance)):
            user_data = request.session.get('user_data')
            if not user_data:
                return RedirectResponse(url="/", status_code=303)

            uid = user_data.get('uid')
            lovense_user = app_instance.client.get_user(uid)
            lovense_user_data = lovense_user.data
            toys = lovense_user_data.get('toys', {})
            if not uid or not lovense_user or not toys:
                return HTMLResponse(content="User not authenticated or no toys connected.", status_code=400)

            nomis = user_data.get('nomis', {})
            if nomi_id not in nomis:
                return HTMLResponse(content="Invalid Nomi ID.", status_code=400)

            # Retrieve chat messages for this Nomi
            chat_threads = user_data.get('chat_threads', {})
            messages = chat_threads.get(nomi_id, [])

            context = {
                'request': request,
                'uid': uid,
                'nomi_id': nomi_id,
                'nomi_name': nomis[nomi_id]['name'],
                'nomis': nomis,
                'messages': messages,
            }
            return templates.TemplateResponse("chat.html", context)

        @web_app.post("/send-chat-message", response_class=HTMLResponse)
        async def send_chat_message(request: Request, app_instance=Depends(get_app_instance)):
            form = await request.form()
            uid = form.get('uid')
            nomi_id = form.get('nomi_id')
            message_text = form.get('message_text')

            user_data = request.session.get('user_data')
            ud_uid = user_data.get('uid')
            ud_nomis = user_data.get('nomis', {})
            chat_threads = user_data.get('chat_threads', {})

            user = app_instance.client.get_user(uid)
            if not user or 'toys' not in user.data:
                return HTMLResponse(content="User not authenticated or no toys connected.", status_code=400)

            if not uid or not nomi_id or not message_text:
                return HTMLResponse(content="Invalid form data.", status_code=400)

            if uid != user.uid:
                return HTMLResponse(content="Invalid user ID.", status_code=400)

            nomis = ud_nomis
            if nomi_id not in nomis:
                return HTMLResponse(content="Invalid Nomi ID.", status_code=400)

            nomi_api_key = user_data.get('nomi_api_key')
            nomi_client = NomiClient(nomi_api_key)

            if nomi_id not in chat_threads: # If this is a new chat thread, add the introduction message
                message_text = nomi_client.introduction_message + "\n\n" + message_text

            # Send message to Nomi AI
            try:
                response = await nomi_client.send_message(nomi_id, message_text)
                sent_message = response.get('sentMessage', {})
                reply_message = response.get('replyMessage', {})
            except Exception as e:
                return HTMLResponse(content=f"Error communicating with Nomi AI: {str(e)}", status_code=500)

            # Parse Nomi AI's response to extract commands
            toys=user.data.get('toys', {})
            if "_test_" in toys:
                logger.info("Test mode enabled. Skipping command execution.")
                command = None
            else:
                command = parse_nomi_response(reply_message.get('text', ''))

            if command:
                # Send command to Lovense device
                toy_id = list(toys.keys())[0]  # one toy is enough for anyone
                try:
                    response = await app_instance.client.control_toy_server(uid, action=command['action'], time_sec=command['timeSec'], toy_id=toy_id)
                    # Maybe handle response if necessary
                except Exception as e:
                    return HTMLResponse(content=f"Error sending command to device: {str(e)}", status_code=500)

            # Update message history
            messages = chat_threads.setdefault(nomi_id, [])
            messages.append({'sender': 'user', 'text': sent_message.get('text')})
            messages.append({'sender': 'nomi', 'text': reply_message.get('text')})

            # Update the session
            # request.session['user_data'] = user_data
            #app_instance.client.create_or_update_user(uid, user.data)

            context = {
                'request': request,
                'uid': uid,
                'nomi_id': nomi_id,
                'nomi_name': nomis[nomi_id]['name'],
                'nomis': nomis,
                'messages': messages,
            }
            return templates.TemplateResponse("chat.html", context)
    
        
        # Assign the web_app to the instance variable
        self.web_app = web_app



