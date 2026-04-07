from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies import get_current_active_user, get_songlist_service
from app.api.schemas.songlist import (
    SonglistCreateRequest,
    SonglistResponse,
    SonglistUpdateRequest,
)
from app.core.entities.user import User
from app.core.exceptions import PermissionDeniedError, SonglistNotFoundError
from app.service.songlist_service import SonglistService

router = APIRouter(prefix='/songlists', tags=['songlists'])


@router.get('', response_model=list[SonglistResponse])
async def get_songlists(
    user: Annotated[User, Depends(get_current_active_user)],
    songlist_service: Annotated[SonglistService, Depends(get_songlist_service)],
):
    """List all songlists belonging to the authenticated user."""
    songlists = await songlist_service.get_user_songlists(user.id)
    return [SonglistResponse.from_entity(s) for s in songlists]


@router.post('', response_model=SonglistResponse, status_code=status.HTTP_201_CREATED)
async def create_songlist(
    request: SonglistCreateRequest,
    user: Annotated[User, Depends(get_current_active_user)],
    songlist_service: Annotated[SonglistService, Depends(get_songlist_service)],
):
    """Create a new songlist for the authenticated user."""
    songlist = await songlist_service.create_songlist(
        user_id=user.id,
        title=request.title,
        song_sid=request.song_sid,
        is_private=request.is_private,
    )
    return SonglistResponse.from_entity(songlist)


@router.get('/{out_id}', response_model=SonglistResponse)
async def get_songlist(
    out_id: str,
    user: Annotated[User, Depends(get_current_active_user)],
    songlist_service: Annotated[SonglistService, Depends(get_songlist_service)],
):
    """Get a songlist by its external ID. Returns 403 for private lists owned by others."""
    try:
        songlist = await songlist_service.get_songlist(out_id, user.id)
        return SonglistResponse.from_entity(songlist)
    except SonglistNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Songlist not found') from None
    except PermissionDeniedError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Access denied') from None


@router.patch('/{out_id}', response_model=SonglistResponse)
async def update_songlist(
    out_id: str,
    request: SonglistUpdateRequest,
    user: Annotated[User, Depends(get_current_active_user)],
    songlist_service: Annotated[SonglistService, Depends(get_songlist_service)],
):
    """Partially update a songlist. Only provided fields are applied."""
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
        return SonglistResponse.from_entity(songlist)
    except SonglistNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Songlist not found') from None
    except PermissionDeniedError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Access denied') from None


@router.delete('/{out_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_songlist(
    out_id: str,
    user: Annotated[User, Depends(get_current_active_user)],
    songlist_service: Annotated[SonglistService, Depends(get_songlist_service)],
):
    """Delete a songlist. Returns 204 on success."""
    try:
        await songlist_service.delete_songlist(out_id, user.id)
    except SonglistNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Songlist not found') from None
    except PermissionDeniedError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Access denied') from None


@router.put('/{out_id}/songs/{song_sid}', response_model=SonglistResponse)
async def add_song(
    out_id: str,
    song_sid: str,
    user: Annotated[User, Depends(get_current_active_user)],
    songlist_service: Annotated[SonglistService, Depends(get_songlist_service)],
):
    """Add a song to a songlist. Idempotent — adding an existing song is a no-op."""
    try:
        songlist = await songlist_service.add_song(out_id, song_sid, user.id)
        return SonglistResponse.from_entity(songlist)
    except SonglistNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Songlist not found') from None
    except PermissionDeniedError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Access denied') from None


@router.delete('/{out_id}/songs/{song_sid}', response_model=SonglistResponse)
async def remove_song(
    out_id: str,
    song_sid: str,
    user: Annotated[User, Depends(get_current_active_user)],
    songlist_service: Annotated[SonglistService, Depends(get_songlist_service)],
):
    """Remove a song from a songlist. Idempotent — removing an absent song is a no-op."""
    try:
        songlist = await songlist_service.remove_song(out_id, song_sid, user.id)
        return SonglistResponse.from_entity(songlist)
    except SonglistNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Songlist not found') from None
    except PermissionDeniedError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Access denied') from None
