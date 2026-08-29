from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.database.session import get_db
from app.models.agent import Agent
from app.schemas.agent import AgentCreate, AgentResponse, AgentCreateResponse
from app.core.security import generate_api_key, hash_api_key

router = APIRouter(prefix="/agents", tags=["agents"])


@router.post("", response_model=AgentCreateResponse, status_code=201)
def register_agent(payload: AgentCreate, db: Session = Depends(get_db)):
    raw_key = generate_api_key()
    agent = Agent(**payload.model_dump(), api_key_hash=hash_api_key(raw_key))
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

    response = AgentCreateResponse(
        id=agent.id,
        agent_id=agent.agent_id,
        name=agent.name,
        department=agent.department,
        purpose=agent.purpose,
        risk_level=agent.risk_level,
        created_at=agent.created_at,
        api_key=raw_key
    )

    return response


@router.get("", response_model=list[AgentResponse])
def list_agents(db: Session = Depends(get_db)):
    return db.query(Agent).all()


@router.get("/{agent_id}", response_model=AgentResponse)
def get_agent(agent_id: str, db: Session = Depends(get_db)):
    agent = db.query(Agent).filter(Agent.agent_id == agent_id).first()

    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")

    return agent