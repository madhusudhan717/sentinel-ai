from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.database.session import get_db
from app.models.agent import Agent
from app.models.role import Role
from app.schemas.agent import AgentCreate, AgentResponse, AgentCreateResponse
from app.core.security import generate_api_key, hash_api_key

router = APIRouter(prefix="/agents", tags=["agents"])


@router.post("", response_model=AgentCreateResponse, status_code=201)
def register_agent(payload: AgentCreate, db: Session = Depends(get_db)):

    # Find the role if role_name was provided
    role_id = None

    if payload.role_name:
        role = db.query(Role).filter(Role.name == payload.role_name).first()

        if not role:
            raise HTTPException(
                status_code=404,
                detail=f"Role '{payload.role_name}' not found"
            )

        role_id = role.id

    # Generate API key
    raw_key = generate_api_key()

    # Remove role_name because Agent model doesn't have role_name column
    agent_data = payload.model_dump(exclude={"role_name"})

    # Create agent
    agent = Agent(
        **agent_data,
        api_key_hash=hash_api_key(raw_key),
        role_id=role_id
    )

    db.add(agent)

    try:
        db.commit()

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=409,
            detail=f"Agent with agent_id '{payload.agent_id}' already exists"
        )

    db.refresh(agent)

    # Create response
    response = AgentCreateResponse.model_validate(
        agent,
        from_attributes=True
    )

    # IMPORTANT:
    # api_key is not stored directly in the database.
    # We add the original key only to the response.
    response.api_key = raw_key

    return response


@router.get("", response_model=list[AgentResponse])
def list_agents(db: Session = Depends(get_db)):
    return db.query(Agent).all()


@router.get("/{agent_id}", response_model=AgentResponse)
def get_agent(agent_id: str, db: Session = Depends(get_db)):

    agent = (
        db.query(Agent)
        .filter(Agent.agent_id == agent_id)
        .first()
    )

    if not agent:
        raise HTTPException(
            status_code=404,
            detail="Agent not found"
        )

    return agent