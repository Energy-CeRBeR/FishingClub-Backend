import uvicorn
from fastapi import FastAPI

from src.users.routers import router as users_router
from src.reports.routers import router as reports_router
from src.admin.routers import router as admin_router

app = FastAPI(
    title="FishingClub API"
)

app.include_router(users_router)
app.include_router(reports_router)
app.include_router(admin_router)

if __name__ == "__main__":
    uvicorn.run(
        "src.main:app",
    )
