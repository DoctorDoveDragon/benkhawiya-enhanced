from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import os
from pathlib import Path
from dotenv import load_dotenv
import logging
from contextlib import asynccontextmanager
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.backend.database import AsyncSessionLocal, get_db, init_db
from app.backend.models.cosmic_principle import CosmicPrinciple
from app.backend.seeds.cosmic_principles import seed_cosmic_principles
from app.backend.services.langchain_service import EnhancedLangChainService

BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

langchain_service = EnhancedLangChainService()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("🌌 Benkhawiya Enhanced AI Cultural Consultant Starting Up")
    await langchain_service.initialize()
    await init_db()
    async with AsyncSessionLocal() as db:
        await seed_cosmic_principles(db)
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

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/api/status")
async def status():
    return {
        "message": "🌌 Benkhawiya Enhanced AI Cultural Consultant",
        "status": "operational",
        "version": "2.0.0",
        "cosmic_bridge": "active"
    }

@app.get("/health")
async def health_check(db: AsyncSession = Depends(get_db)):
    db_status = "disconnected"
    try:
        await db.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception as exc:
        logger.warning("Health check – DB unreachable: %s", exc)

    return {
        "status": "healthy" if db_status == "connected" else "degraded",
        "services": {
            "database": db_status,
            "langchain": "initialized" if langchain_service.initialized else "pending",
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
            response = await langchain_service.process_query(data)
            await websocket.send_text(response)
    except WebSocketDisconnect:
        logger.info("Client disconnected")

@app.get("/api/cosmic-principles")
async def get_cosmic_principles(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(CosmicPrinciple).order_by(CosmicPrinciple.id))
    principles = result.scalars().all()
    return {
        "principles": [
            {"name": p.name, "meaning": p.meaning, "aspect": p.aspect}
            for p in principles
        ]
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
