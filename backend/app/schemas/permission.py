import uuid
from pydantic import BaseModel


class PermissionCreate(BaseModel):
    name: str
    description: str | None = None


class PermissionResponse(BaseModel):
    id: uuid.UUID
    name: str
    description: str | None = None

    class Config:
        from_attributes = True