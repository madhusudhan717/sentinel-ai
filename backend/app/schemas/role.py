import uuid
from pydantic import BaseModel

from app.schemas.permission import PermissionResponse


class RoleCreate(BaseModel):
    name: str
    description: str | None = None


class RoleResponse(BaseModel):
    id: uuid.UUID
    name: str
    description: str | None = None
    permissions: list[PermissionResponse] = []

    class Config:
        from_attributes = True


class AssignPermissionsRequest(BaseModel):
    permission_names: list[str]