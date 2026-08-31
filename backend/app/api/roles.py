from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.database.session import get_db
from app.models.role import Role
from app.models.permission import Permission
from app.schemas.role import RoleCreate, RoleResponse, AssignPermissionsRequest

router = APIRouter(prefix="/roles", tags=["roles"])


@router.post("", response_model=RoleResponse, status_code=201)
def create_role(payload: RoleCreate, db: Session = Depends(get_db)):
    role = Role(**payload.model_dump())
    db.add(role)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail=f"Role '{payload.name}' already exists")
    db.refresh(role)
    return role


@router.get("", response_model=list[RoleResponse])
def list_roles(db: Session = Depends(get_db)):
    return db.query(Role).all()


@router.get("/{role_name}", response_model=RoleResponse)
def get_role(role_name: str, db: Session = Depends(get_db)):
    role = db.query(Role).filter(Role.name == role_name).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return role


@router.post("/{role_name}/permissions", response_model=RoleResponse)
def assign_permissions(role_name: str, payload: AssignPermissionsRequest, db: Session = Depends(get_db)):
    role = db.query(Role).filter(Role.name == role_name).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")

    permissions = db.query(Permission).filter(Permission.name.in_(payload.permission_names)).all()
    found_names = {p.name for p in permissions}
    missing = set(payload.permission_names) - found_names
    if missing:
        raise HTTPException(status_code=404, detail=f"Permissions not found: {', '.join(missing)}")

    role.permissions = permissions  # replaces the full set; simple and predictable for this MVP
    db.commit()
    db.refresh(role)
    return role