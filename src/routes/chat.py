import uuid
import os
from fastapi import APIRouter, FastAPI, WebSocket, Request, HTTPException, Depends
from utils.console import pretty_print, MessageType
from src.socket.connection import ConnectionManager
from ..socket.utils import get_token
from server.src.redis.producer import Producer
from server.src.redis.config import Redis

chat = APIRouter()
manager = ConnectionManager()
redis = Redis()

# @route   POST /token
# @desc    Route generating chat token
# @access  Public

@chat.post("/token")
async def token_generator(name: str, request: Request):
    if not name:
        pretty_print("Invalid name provided", MessageType.FATAL)
        raise HTTPException(status_code=400, detail={
            "loc": "name", "msg": "Enter a valid name"
        })

    token = str(uuid.uuid4())
    data = {"name": name, "token": token}

    pretty_print(f"Token generated for {name}: {token}", MessageType.SUCCESS)
    return data

# @route   POST /refresh_token
# @desc    Route to refresh token
# @access  Public

@chat.post("/refresh_token")
async def refresh_token(request: Request):
    return None

# @route   Websocket /chat
# @desc    Socket for chatbot
# @access  Public

@chat.websocket("/chat")
async def websocket_endpoint(websocket: WebSocket, token: str = Depends(get_token)):
    await manager.connect(websocket)
    redis_client = await redis.create_connection()
    producer = Producer(redis_client)

    try:
        while True:
            data = await websocket.receive_text()
            print(data)
            stream_data = {}
            stream_data[token] = data
            await producer.add_to_stream(stream_data, "message_channel")
            await manager.send_personal_message(f"Response: Simulating response from the GPT service", websocket)

    except WebSocketDisconnect:
        manager.disconnect(websocket)