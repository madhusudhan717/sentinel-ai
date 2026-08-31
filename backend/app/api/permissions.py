from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.database.session import get_db
from app.models.permission import Permission
from app.schemas.permission import PermissionCreate, PermissionResponse

router = APIRouter(prefix="/permissions", tags=["permissions"])


@router.post("", response_model=PermissionResponse, status_code=201)
def create_permission(payload: PermissionCreate, db: Session = Depends(get_db)):
    permission = Permission(**payload.model_dump())
    db.add(permission)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail=f"Permission '{payload.name}' already exists")
    db.refresh(permission)
    return permission


@router.get("", response_model=list[PermissionResponse])
def list_permissions(db: Session = Depends(get_db)):
    return db.query(Permission).all()