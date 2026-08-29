import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AgentCreate(BaseModel):
    agent_id: str
    name: str
    department: str
    purpose: str
    risk_level: str = "medium"


class AgentResponse(BaseModel):
    id: uuid.UUID
    agent_id: str
    name: str
    department: str
    purpose: str
    risk_level: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)