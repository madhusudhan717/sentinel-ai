from fastapi import FastAPI, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.database.session import get_db, engine, Base
from app.models.agent import Agent  # noqa: F401 - import so Base knows about this table
from app.api import agents

app = FastAPI(
    title="Sentinel-AI",
    description="Session-Aware Runtime Governance and Enterprise Authorization Platform for Autonomous AI Agents",
    version="0.1.0",
)


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)


app.include_router(agents.router)


@app.get("/")
def root():
    return {"status": "ok", "service": "Sentinel-AI Gateway"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.get("/health/db")
def health_check_db(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {"status": "healthy", "database": "connected"}