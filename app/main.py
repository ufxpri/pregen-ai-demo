# server.py
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from langserve import add_routes

from app.settings import settings

from app.services.presentation import chain as feedback_chain

app = FastAPI(
    title="pregen ai server",
    version="0.1",
    description="ai server for pregen's presentation feedback algorithm"
)

# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Mount the static directory to serve static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            # Receive audio data as bytes
            data = await websocket.receive_bytes()
            # Process the received audio data here
            print(f"Received audio data of length {len(data)}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await websocket.close()


add_routes(app, feedback_chain, path="/feedback_chain")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
