from fastapi import FastAPI, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.database.session import get_db, engine, Base
from app.models.agent import Agent  # noqa: F401
from app.models.role import Role  # noqa: F401
from app.models.permission import Permission  # noqa: F401
from app.api import agents, roles, permissions

app = FastAPI(
    title="Sentinel-AI",
    description="Session-Aware Runtime Governance and Enterprise Authorization Platform for Autonomous AI Agents",
    version="0.1.0",
)


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)


app.include_router(agents.router)
app.include_router(roles.router)
app.include_router(permissions.router)


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