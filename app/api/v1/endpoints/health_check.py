from typing import Any

from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session  # type: ignore
from starlette.requests import Request

from app.api import deps
from app.schemas.v1.health_check import HealthCheck

router = APIRouter()


@router.get("/", response_model=HealthCheck, tags=["health check"])
def health_check(
    *, request: Request, session: Session = Depends(deps.get_db)
) -> Any:
    session.execute("SELECT 1")
    return HealthCheck(message="OK")
