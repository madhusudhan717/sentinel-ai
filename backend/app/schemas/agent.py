import uuid
from datetime import datetime
from pydantic import BaseModel


class AgentCreate(BaseModel):
    agent_id: str
    name: str
    department: str
    purpose: str
    risk_level: str = "medium"
    role_name: str | None = None


class AgentResponse(BaseModel):
    id: uuid.UUID
    agent_id: str
    name: str
    department: str
    purpose: str
    risk_level: str
    created_at: datetime

    class Config:
        from_attributes = True


class AgentCreateResponse(AgentResponse):
    api_key: str