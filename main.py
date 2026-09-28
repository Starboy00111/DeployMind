from fastapi import FastAPI

app = FastAPI(
    title="DeployMind",
    description="Self-Learning DevOps Pipeline Agent",
    version="1.0.0"
)

@app.get("/")
def home():
    return {
        "project": "DeployMind",
        "status": "Backend running",
        "message": "Self-Learning DevOps Pipeline Agent is ready"
    }