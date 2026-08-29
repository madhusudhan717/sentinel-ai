from fastapi import Header, HTTPException, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.agent import Agent
from app.core.security import hash_api_key
from app.config import settings


def get_current_agent(
    x_api_key: str = Header(..., alias="X-API-Key"),
    db: Session = Depends(get_db),
) -> Agent:
    """Validates the API key sent in the X-API-Key header and returns the matching Agent."""
    key_hash = hash_api_key(x_api_key)
    agent = db.query(Agent).filter(Agent.api_key_hash == key_hash).first()
    if not agent:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return agent


def verify_admin(x_admin_password: str = Header(..., alias="X-Admin-Password")):
    """Validates the admin password for human-approval/dashboard routes."""
    if x_admin_password != settings.admin_password:
        raise HTTPException(status_code=401, detail="Invalid admin password")
    return True