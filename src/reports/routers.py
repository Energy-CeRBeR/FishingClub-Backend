from fastapi import APIRouter

router = APIRouter(tags=["fishing"], prefix="/fishing")


@router.post("/reports/new")
async def create_report(

):
    pass


@router.get("/reports/all")
async def get_all_reports():
    pass
