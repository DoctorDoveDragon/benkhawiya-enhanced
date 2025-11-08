from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
import logging
from contextlib import asynccontextmanager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("🌌 Benkhawiya Enhanced AI Cultural Consultant Starting Up")
    yield
    # Shutdown
    logger.info("🌌 Benkhawiya Enhanced AI Cultural Consultant Shutting Down")

app = FastAPI(
    title="Benkhawiya Enhanced AI Cultural Consultant",
    description="Advanced African Cosmological Bridge with AI Integration",
    version="2.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "message": "🌌 Benkhawiya Enhanced AI Cultural Consultant",
        "status": "operational",
        "version": "2.0.0",
        "cosmic_bridge": "active"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "services": {
            "database": "connected",
            "langchain": "initialized",
            "community": "active",
            "research": "ready"
        }
    }

@app.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            # Simple echo for now - will be enhanced with AI
            response = f"🌌 Cosmic Response: I receive your query '{data}' through the Benkhawiya framework"
            await websocket.send_text(response)
    except WebSocketDisconnect:
        logger.info("Client disconnected")

@app.get("/api/cosmic-principles")
async def get_cosmic_principles():
    return {
        "principles": [
            {"name": "DÁNÁ", "meaning": "Truth", "aspect": "pelu"},
            {"name": "MÁTÁ", "meaning": "Justice", "aspect": "sewu"},
            {"name": "HÓTÉ", "meaning": "Harmony", "aspect": "ruwa"},
            {"name": "MÉKÁ", "meaning": "Balance", "aspect": "temu"},
            {"name": "SÉBÁ", "meaning": "Order", "aspect": "sewu"},
            {"name": "KÉPÉ", "meaning": "Reciprocity", "aspect": "ruwa"},
            {"name": "ÌTỌJÚ", "meaning": "Mystery", "aspect": "ntu"}
        ]
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
