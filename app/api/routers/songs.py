from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.api.dependencies import get_current_active_user, get_current_manager, get_song_service
from app.api.schemas.song import SongCreateRequest, SongResponse, SongUpdateRequest
from app.core.entities.user import User
from app.core.enums import Language, Tonality
from app.service.song_service import SongService

router = APIRouter(prefix='/songs', tags=['songs'])


@router.get('/random', response_model=list[SongResponse])
async def get_random_songs(
    song_service: Annotated[SongService, Depends(get_song_service)],
    _user: Annotated[User, Depends(get_current_active_user)],
    amount: int = Query(default=6),
) -> list[SongResponse]:
    versions = await song_service.get_random(amount)
    return [SongResponse.from_entity(v) for v in versions]


@router.get('', response_model=list[SongResponse])
async def list_songs(
    song_service: Annotated[SongService, Depends(get_song_service)],
    _user: Annotated[User, Depends(get_current_active_user)],
    title: str = Query(default=''),
    lyrics: str = Query(default=''),
    lang: Language | None = None,
    collection: str = Query(default=''),
    tonality: Tonality | None = None,
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
) -> list[SongResponse]:
    versions = await song_service.list_songs(
        title=title,
        lyrics=lyrics,
        lang=lang or '',
        collection=collection,
        tonality=tonality or '',
        limit=limit,
        offset=offset,
    )
    return [SongResponse.from_entity(v) for v in versions]


@router.post('', response_model=SongResponse, status_code=status.HTTP_201_CREATED)
async def create_song(
    request: SongCreateRequest,
    _manager: Annotated[User, Depends(get_current_manager)],
    song_service: Annotated[SongService, Depends(get_song_service)],
) -> SongResponse:
    created = await song_service.create_song(request.to_version_entity(), request.to_work_entity())
    return SongResponse.from_entity(created)


@router.get('/{sid}', response_model=SongResponse)
async def get_song(
    sid: str,
    song_service: Annotated[SongService, Depends(get_song_service)],
    _user: Annotated[User, Depends(get_current_active_user)],
) -> SongResponse:
    version = await song_service.get_by_sid(sid)
    if version is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Song not found')
    return SongResponse.from_entity(version)


@router.patch('/{sid}', response_model=SongResponse)
async def update_song(
    sid: str,
    request: SongUpdateRequest,
    _manager: Annotated[User, Depends(get_current_manager)],
    song_service: Annotated[SongService, Depends(get_song_service)],
) -> SongResponse:
    version = request.to_version_entity()
    updated = await song_service.update_song(sid, version)
    if updated is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Song not found')
    return SongResponse.from_entity(updated)


@router.delete('/{sid}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_song(
    sid: str,
    _manager: Annotated[User, Depends(get_current_manager)],
    song_service: Annotated[SongService, Depends(get_song_service)],
) -> None:
    success = await song_service.delete_song(sid)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Song not found')
