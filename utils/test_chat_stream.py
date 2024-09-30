import httpx
import asyncio
import websockets
from utils.console import pretty_print, MessageType

async def get_token(name: str):
    async with httpx.AsyncClient() as client:
        response = await client.post(f"http://localhost:3500/token?name={name}")
        response.raise_for_status()
        token = response.json()["token"]
        pretty_print(f"Token received: {token}", MessageType.INFO)
        return token

async def test_chat_stream(token: str):
    uri = f"ws://localhost:3500/chat?token={token}"
    async with websockets.connect(uri) as websocket:
        for i in range(10):  # Send 10 HELLO messages
            await websocket.send("HELLO")
            response = await websocket.recv()
            pretty_print(f"Response from chat: {response}", MessageType.INFO)
            await asyncio.sleep(1)  # Wait for 1 second between messages

async def main():
    name = "pythuto"
    try:
        token = await get_token(name)
        await test_chat_stream(token)
    except httpx.HTTPStatusError as e:
        pretty_print(f"HTTP error occurred: {e}", MessageType.FATAL)
    except websockets.exceptions.WebSocketException as e:
        pretty_print(f"WebSocket error occurred: {e}", MessageType.FATAL)
    except Exception as e:
        pretty_print(f"An unexpected error occurred: {e}", MessageType.FATAL)

if __name__ == "__main__":
    asyncio.run(main())