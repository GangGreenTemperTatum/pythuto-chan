from fastapi import FastAPI, Request
import uvicorn
import os
from dotenv import load_dotenv
from utils.console import pretty_print, MessageType
from src.routes.chat import chat

load_dotenv()

api = FastAPI()
api.include_router(chat)

@api.get("/test")
async def root():
    return {"msg": "API is Online"}

if __name__ == "__main__":
    app_env = os.environ.get('APP_ENV')
    huggingface_inference_token = os.environ.get('HUGGINFACE_INFERENCE_TOKEN')

    pretty_print(f"APP_ENV: {app_env}", MessageType.INFO)
    
    if not huggingface_inference_token:
        pretty_print("HUGGINFACE_INFERENCE_TOKEN is not set. Please set it in your environment variables or .env file.", MessageType.FATAL)
    
    if app_env == "development":
        uvicorn.run("main:api", host="0.0.0.0", port=3500, workers=4, reload=True)
    else:
        pretty_print("Server not started. APP_ENV is not 'development'.", MessageType.WARN)