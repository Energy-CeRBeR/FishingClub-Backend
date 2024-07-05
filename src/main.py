import uvicorn
from fastapi import FastAPI

from src.users.routers import router as user_router

app = FastAPI(
    title="FishingClub api"
)

app.include_router(user_router)

if __name__ == "__main__":
    uvicorn.run(
        "src.main:app",
    )
