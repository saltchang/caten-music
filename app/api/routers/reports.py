from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies import get_current_active_user, get_report_service
from app.api.schemas.report import ReportCreateRequest, ReportResponse
from app.core.entities.user import User
from app.core.exceptions import InvalidInputError
from app.service.report_service import ReportService

router = APIRouter(prefix='/reports', tags=['reports'])


@router.post('/', response_model=ReportResponse, status_code=status.HTTP_201_CREATED)
async def create_report(
    request: ReportCreateRequest,
    user: Annotated[User, Depends(get_current_active_user)],
    report_service: Annotated[ReportService, Depends(get_report_service)],
):
    try:
        report = await report_service.create_report(
            description=request.description,
            song_sid=request.song_sid,
            user_id=user.id,
        )
        return ReportResponse.from_entity(report)
    except InvalidInputError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from None
