from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies import get_current_active_user, get_songlist_service
from app.api.schemas.common import MessageResponse
from app.api.schemas.songlist import (
    SonglistCreateRequest,
    SonglistResponse,
    SonglistToggleResponse,
    SonglistUpdateRequest,
)
from app.core.entities.user import User
from app.core.exceptions import PermissionDeniedError, SonglistNotFoundError
from app.service.songlist_service import SonglistService

router = APIRouter(prefix='/songlists', tags=['songlists'])


@router.get('/', response_model=list[SonglistResponse])
async def get_songlists(
    user: Annotated[User, Depends(get_current_active_user)],
    songlist_service: Annotated[SonglistService, Depends(get_songlist_service)],
):
    songlists = await songlist_service.get_user_songlists(user.id)
    return [_songlist_to_response(s) for s in songlists]


@router.post('/', response_model=SonglistResponse, status_code=status.HTTP_201_CREATED)
async def create_songlist(
    request: SonglistCreateRequest,
    user: Annotated[User, Depends(get_current_active_user)],
    songlist_service: Annotated[SonglistService, Depends(get_songlist_service)],
):
    songlist = await songlist_service.create_songlist(
        user_id=user.id,
        title=request.title,
        song_sid=request.song_sid,
        is_private=request.is_private,
    )
    return _songlist_to_response(songlist)


@router.get('/{out_id}', response_model=SonglistResponse)
async def get_songlist(
    out_id: str,
    user: Annotated[User, Depends(get_current_active_user)],
    songlist_service: Annotated[SonglistService, Depends(get_songlist_service)],
):
    try:
        songlist = await songlist_service.get_songlist(out_id, user.id)
        return _songlist_to_response(songlist)
    except SonglistNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Songlist not found') from None
    except PermissionDeniedError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Access denied') from None


@router.put('/{out_id}', response_model=SonglistResponse)
async def update_songlist(
    out_id: str,
    request: SonglistUpdateRequest,
    user: Annotated[User, Depends(get_current_active_user)],
    songlist_service: Annotated[SonglistService, Depends(get_songlist_service)],
):
    try:
        songlist = await songlist_service.edit_songlist(
            out_id=out_id,
            user_id=user.id,
            title=request.title,
            description=request.description,
            is_private=request.is_private,
            is_archived=request.is_archived,
            songs_sid_list=request.songs_sid_list,
        )
        return _songlist_to_response(songlist)
    except SonglistNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Songlist not found') from None
    except PermissionDeniedError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Access denied') from None


@router.delete('/{out_id}', response_model=MessageResponse)
async def delete_songlist(
    out_id: str,
    user: Annotated[User, Depends(get_current_active_user)],
    songlist_service: Annotated[SonglistService, Depends(get_songlist_service)],
):
    try:
        await songlist_service.delete_songlist(out_id, user.id)
        return MessageResponse(message='Songlist deleted successfully')
    except SonglistNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Songlist not found') from None
    except PermissionDeniedError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Access denied') from None


@router.put('/{out_id}/songs/{song_sid}', response_model=SonglistToggleResponse)
async def toggle_song(
    out_id: str,
    song_sid: str,
    user: Annotated[User, Depends(get_current_active_user)],
    songlist_service: Annotated[SonglistService, Depends(get_songlist_service)],
):
    try:
        result = await songlist_service.toggle_song(out_id, song_sid, user.id)
        return SonglistToggleResponse(**result)
    except SonglistNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Songlist not found') from None
    except PermissionDeniedError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Access denied') from None


def _songlist_to_response(songlist):
    return SonglistResponse(
        id=songlist.id,
        out_id=songlist.out_id,
        title=songlist.title,
        description=songlist.description,
        user_id=songlist.user_id,
        songs_sid_list=songlist.songs_sid_list,
        songs_amount=songlist.songs_amount,
        created_time=songlist.created_time,
        edited_time=songlist.edited_time,
        is_private=songlist.is_private,
        is_archived=songlist.is_archived,
    )
