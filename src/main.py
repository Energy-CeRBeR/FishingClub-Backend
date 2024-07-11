import uvicorn
from fastapi import FastAPI

from src.users.routers import router as users_router
from src.reports.routers import router as reports_router

app = FastAPI(
    title="FishingClub api"
)

app.include_router(users_router)
app.include_router(reports_router)

if __name__ == "__main__":
    uvicorn.run(
        "src.main:app",
    )
