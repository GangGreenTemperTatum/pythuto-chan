from src.redis.config import Redis
import asyncio
from src.model.gptj import GPT
from src.redis.cache import Cache

redis = Redis()

async def main():

    json_client = redis.create_rejson_connection()

    await Cache(json_client).add_message_to_cache(token="eb6646a7-f358-4e8c-b73a-92047b6e7dbb", source="human", message_data={
        "id": "3",
        "msg": "I would like to go to the moon to, would you take me?",
        "timestamp": "2022-07-16 13:20:01.092109"
    })

    data = await Cache(json_client).get_chat_history(token="eb6646a7-f358-4e8c-b73a-92047b6e7dbb")

    print(data)

    message_data = data['messages'][-4:] # the integer gathers the prior X number of messages in the cache to give the model context

    input = ["" + i['msg'] for i in message_data]
    input = " ".join(input)

    res = GPT().query(input=input)

    msg = Message(
        msg=res
    )

    print(msg)
    await Cache(json_client).add_message_to_cache(token="eb6646a7-f358-4e8c-b73a-92047b6e7dbb", source="bot", message_data=msg.dict())

if __name__ == "__main__":
    asyncio.run(main())

