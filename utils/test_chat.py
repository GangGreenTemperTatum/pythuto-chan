import httpx
import asyncio
import websockets

async def get_token(name: str):
    async with httpx.AsyncClient() as client:
        response = await client.post(f"http://localhost:3500/token?name={name}")
        response.raise_for_status()
        return response.json()["token"]

async def test_chat(token: str):
    uri = f"ws://localhost:3500/chat?token={token}"
    async with websockets.connect(uri) as websocket:
        await websocket.send("Hello Bot")
        response = await websocket.recv()
        print(f"Response from chat: {response}")

async def main():
    name = "pythuto"
    token = await get_token(name)
    print(f"Token received: {token}")
    await test_chat(token)

if __name__ == "__main__":
    asyncio.run(main())