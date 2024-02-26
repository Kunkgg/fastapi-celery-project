from fastapi import APIRouter

whitebox_reports_router = APIRouter(
    prefix="/whitebox-reports",
)

from . import views, models, tasks