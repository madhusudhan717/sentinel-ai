from app.models.agent import Agent


def agent_has_permission(agent: Agent, permission_name: str) -> bool:
    """Fail-closed: no role or no matching permission both mean 'not authorized'."""
    if not agent.role:
        return False
    return any(p.name == permission_name for p in agent.role.permissions)