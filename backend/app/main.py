from fastapi import FastAPI

app = FastAPI(
    title="AI Personal Knowledge Assitance",
    description="API for uploading, searching and asking questions about personal documents.",
    version="0.1.0"
)

@app.get("/")
async def root() -> dict[str, str]:
    return {
        "message": "AI Personal Knowledge Assistat API is running"
    }

@app.get("/health")
async def health_check() -> dict[str, str]:
    return {
        "status": "healthy"
    }