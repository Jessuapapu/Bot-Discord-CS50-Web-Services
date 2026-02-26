from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from Singleton import EstadoGlobal
from Socket import WebSocket
import socketio

import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY",None)


if API_KEY is None:
    print("API KEY NO CARGADO")

from routes.main_routes import app_router

# App declaracion 
app = FastAPI()


# declaracion de rutas
app.include_router(app_router)

# Configuración de CORS para FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],    
)


# Envolvemos la app para interceptar las rutas de socket.io
app = socketio.ASGIApp(WebSocket.sio, app)


# declaracion de Singleton
#   SIG = EstadoGlobal.EstadoGlobal()
