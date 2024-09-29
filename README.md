# `pythuto-chan`: Your Local AI Chatbot

<div align="left">
  <img src="media/pythuto-chan-2.jpg" alt="pythuto-chan" width="300"/>
</div>
<br>

`pythuto-chan` is a local AI chatbot application built using Python's FastAPI, HuggingFace's inference API, and Redis for memory storage. Inspired by the beloved anime character Naruto, Pythuto-chan brings the power of AI to your local environment.

## Features

- **FastAPI**: A modern, fast (high-performance) web framework for building APIs with Python.
- **HuggingFace Inference API**: Leverage state-of-the-art machine learning models for natural language processing.
- **Redis Memory Store**: Efficiently store and retrieve conversation history, see the [redis structure](./worker).
  - We isolate our worker environment from the web server so that when the client sends a message to our WebSocket, the web server does not have to handle the request to the third-party service. Also, resources can be freed up for other users.
  - The background communication with the inference API is handled by this worker service, through Redis. Requests from all connected clients are appended to the message queue (producer), while the worker consumes the messages, sends the requests to the inference API, and appends the responses to a response queue. Once the API receives a response, it sends it back to the client. During the trip between the producer and the consumer, the client can send multiple messages, and these messages will be queued up and responded to in order. Ideally, this worker could run on a completely different server in its own environment, but for now, it will run in its own Python environment on our local machine.
- **Local Deployment**: Run the chatbot locally on your machine or host it on dedicated infrastructure.
- **Websockets**: The [asynchronous connections code (`ConnectionManager` class)](src/socket/connections.py) utilizes websockets for multiple session concurrency and also authorizes only valid sessions.

Checkout the [resources folder](./resources) for an OpenAPI schema and import it into Bruno/Postman etc.

## Installation

Follow these steps to set up `pythuto-chan` on your local machine:

1. **Clone the repository**:
    ```sh
    git clone https://github.com/GangGreenTemperTatum/pythuto-chan.git
    cd pythuto-chan
    ```

2. **Create a virtual environment**:
    ```sh
    python3 -m venv pythuto-venv
    source pythuto-venv/bin/activate

    export APP_ENV=development
    export HUGGINGFACE_API_KEY="<YOUR_HUGGINGFACE_API_KEY>"
    ```

Or via an `.env` file, (less preferred) `touch.env && echo "export APP_ENV=development" >> .env`

1. **Install the dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

*Verify the development is not already using the local default port, (`lsof -i :3500`) or (`netstat -an | grep 3500`)*

4. **Local Development Tests**:
   - Run `python3 main.py` to spinup the local environment

    ```sh
    (pythuto-venv) ➜  pythuto-chan git:(master) ✗ python3 main.py           
    INFO:     Will watch for changes in these directories: ['/x/y/git/pythuto-chan']
    INFO:     Uvicorn running on http://0.0.0.0:3500 (Press CTRL+C to quit)
    INFO:     Started reloader process [30333] using statreload
    INFO:     Started server process [30335]
    INFO:     Waiting for application startup.
    INFO:     Application startup complete.
    ``` 

    ```sh
    (pythuto-venv) ➜  pythuto-chan git:(master) ✗ curl -X GET http://localhost:3500/test
    {"msg":"API is Online"}% 
    ...
    INFO:     127.0.0.1:55976 - "GET /test HTTP/1.1" 200 OK
    ```

    **Test Websocket for `/chat` and API Routes**:

    ```sh
    curl -X POST "http://localhost:3500/token?name=pythuto"
    ..
    {"name":"pythuto","token":"cd9df3b7-f035-4df8-b0cf-6bc28c7364e1"}%
    
    ...

    websocat ws://localhost:3500/chat -E -n -k <<< "Hello Bot"
    ..
    INFO:     connection closed
    INFO:     ('127.0.0.1', 64300) - "WebSocket /chat" [accepted]
    INFO:     connection open
    Hello Bot
    ```

5. **Set up Redis**:
    - Install Redis on your machine. For macOS, you can use Homebrew:
        ```sh
        brew install redis
        ```
    - Start the Redis server:
        ```sh
        brew services start redis
        brew services info redis
        ```
    - Test the Redis server:
        ```sh
        redis-cli
        ping
        ```
    - Next open up a new terminal, cd into the worker folder, and create and activate a new Python virtual environment and install requirements:
        ```sh
        cd ./worker
        python3 -m venv redis-venv
        source redis-venv/bin/activate
        
        pip install -r requirements.txt
        ```
    - Add Redis `.env` files in `/worker/.env` (example default local redis setup)
        ```sh
        REDIS_URL=localhost:6379
        REDIS_USER=default
        REDIS_PASSWORD=
        REDIS_HOST=localhost
        REDIS_PORT=6379
        ```
    - Test the redis connection to create a new Redis connection pool, set a simple key "key", and assign a string "value" to it:
        ```sh
        (redis-venv) (pythuto-venv) ➜  worker git:(main) ✗ python3 main.py                
        Redis<ConnectionPool<Connection<host=localhost,port=6379,db=0>>>
        ```

6. **Run the FastAPI application**:
    ```sh
    uvicorn main:app --reload
    ```

## Usage

Once the application is running, you can interact with pythuto-chan via the API endpoints. Open your browser and navigate to `http://127.0.0.1:8000/docs` to access the interactive API documentation.

## Configuration

You can configure the application by modifying the `config.py` file. Key configurations include:

- **HuggingFace API Key**: Set your HuggingFace API key to access the inference API.
- **Redis Configuration**: Adjust Redis connection settings if necessary.

Enjoy chatting with `pythuto-chan`! Believe it! 🍥🦊

## Development 🚧

- JWT authentication / refresh tokens

## Star History 🪐

<div align="left">
  <img src="https://api.star-history.com/svg?repos=GangGreenTemperTatum/pythuto-chan&type=Date" alt="pythuto-chan Star History Chart" width="700"/>
</div>
<br>
<p><a href="https://www.buymeacoffee.com/GangGreenTemperTatum"> <img align="left" src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" height="50" width="210" alt="GangGreenTemperTatum" /></a></p><br><br>