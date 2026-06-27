from fastapi import FastAPI, HTTPException, status
from sqlalchemy.exc import SQLAlchemyError

from app.database import check_database_connection

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

@app.get("/health/database")
def database_health_check() -> dict[str,str]:
    try:
        check_database_connection()
    except SQLAlchemyError as error:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database connection failed"

        ) from error
    
    return {
        "status": "healthy",
        "database": "connected",
    }