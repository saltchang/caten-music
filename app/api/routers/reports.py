from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies import get_current_active_user, get_current_admin, get_report_service
from app.api.schemas.report import ReportCreateRequest, ReportResponse
from app.core.entities.user import User
from app.core.exceptions import InvalidInputError
from app.service.report_service import ReportService

router = APIRouter(prefix='/reports', tags=['reports'])


@router.get('', response_model=list[ReportResponse])
async def list_reports(
    _admin: Annotated[User, Depends(get_current_admin)],
    report_service: Annotated[ReportService, Depends(get_report_service)],
):
    """List all reports. Requires admin role.

    Args:
        _admin: Current authenticated admin (used for authorization).
        report_service: Injected report service.

    Returns:
        List of ReportResponse for all reports.
    """
    reports = await report_service.list_reports()
    return [ReportResponse.from_entity(r) for r in reports]


@router.post('', response_model=ReportResponse, status_code=status.HTTP_201_CREATED)
async def create_report(
    request: ReportCreateRequest,
    user: Annotated[User, Depends(get_current_active_user)],
    report_service: Annotated[ReportService, Depends(get_report_service)],
):
    """Create a new report for a song. Requires an active user.

    Args:
        request: Payload with the report description and song SID.
        user: Current authenticated active user.
        report_service: Injected report service.

    Returns:
        ReportResponse for the newly created report.

    Raises:
        HTTPException: 400 for invalid input.
    """
    try:
        report = await report_service.create_report(
            description=request.description,
            song_sid=request.song_sid,
            user_id=user.id,
        )
        return ReportResponse.from_entity(report)
    except InvalidInputError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from None
