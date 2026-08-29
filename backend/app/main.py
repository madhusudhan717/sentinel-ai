from fastapi import FastAPI

app = FastAPI(
    title="Sentinel-AI",
    description="Session-Aware Runtime Governance and Enterprise Authorization Platform for Autonomous AI Agents",
    version="0.1.0",
)


@app.get("/")
def root():
    return {
        "status": "ok",
        "service": "Sentinel-AI Gateway"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }