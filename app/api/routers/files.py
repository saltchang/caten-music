from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse

from app.api.dependencies import get_current_active_user, get_file_download_service
from app.core.entities.user import User
from app.service.file_service import FileService

router = APIRouter(prefix='/files', tags=['files'])


@router.get('/ppt/{sid}')
async def get_ppt(
    sid: str,
    _user: Annotated[User, Depends(get_current_active_user)],
    file_service: Annotated[FileService, Depends(get_file_download_service)],
):
    url = await file_service.get_ppt_url(sid)
    if url is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='PPT file not found')
    return RedirectResponse(url=url)


@router.get('/sheet/{sid}')
async def get_sheet(
    sid: str,
    _user: Annotated[User, Depends(get_current_active_user)],
    file_service: Annotated[FileService, Depends(get_file_download_service)],
):
    url = await file_service.get_sheet_url(sid)
    if url is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Sheet file not found')
    return RedirectResponse(url=url)
