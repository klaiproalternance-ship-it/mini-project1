import asyncio
import uuid
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, WebSocket, WebSocketDisconnect, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

from api.models import Server, ServerIn, ServerOut
from api.auth import verify_api_key
from api.metrics import get_system_metrics
from api.poller import run_poll_loop, poll_server

# Shared in-memory store for servers
store = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Start the background polling task
    poll_task = asyncio.create_task(run_poll_loop(store, interval=10))
    app.state.poll_task = poll_task
    yield
    # Shutdown: Cancel the task cleanly
    poll_task.cancel()
    try:
        await poll_task
    except asyncio.CancelledError:
        pass

app = FastAPI(title="DevOps Monitoring API", lifespan=lifespan)

# Add CORS middleware to allow Streamlit frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/metrics")
def metrics():
    return get_system_metrics()

@app.websocket("/ws/metrics")
async def ws_metrics(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            current_metrics = get_system_metrics()
            await websocket.send_json(current_metrics)
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        pass
    except Exception:
        pass

@app.post("/servers", response_model=ServerOut, status_code=201)
def create_server(server_in: ServerIn, api_key: str = Depends(verify_api_key)):
    server_id = str(uuid.uuid4())
    server = Server(
        id=server_id,
        name=server_in.name,
        host=server_in.host,
        port=server_in.port,
        status="unknown"
    )
    store[server_id] = server
    return server

@app.get("/servers", response_model=list[ServerOut])
def get_servers(status: str = None):
    servers = list(store.values())
    if status:
        servers = [s for s in servers if s.status.upper() == status.upper()]
    return servers

@app.get("/servers/{id}", response_model=ServerOut)
def get_server(id: str):
    if id not in store:
        raise HTTPException(status_code=404, detail="Server not found")
    return store[id]

@app.delete("/servers/{id}", response_model=ServerOut)
def delete_server(id: str, api_key: str = Depends(verify_api_key)):
    if id not in store:
        raise HTTPException(status_code=404, detail="Server not found")
    return store.pop(id)

@app.post("/servers/{id}/check")
async def check_server(id: str):
    if id not in store:
        raise HTTPException(status_code=404, detail="Server not found")
    server = store[id]
    # Trigger check in the background
    asyncio.create_task(poll_server(id, server.base_url(), store))
    return {"status": "check initiated"}
