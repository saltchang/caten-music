from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.api.dependencies import get_current_active_user, get_song_service
from app.api.schemas.song import SongResponse
from app.core.entities.user import User
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


@router.get('/search', response_model=list[SongResponse])
async def search_songs(
    song_service: Annotated[SongService, Depends(get_song_service)],
    _user: Annotated[User, Depends(get_current_active_user)],
    mode: str = Query(...),
    q: str = Query(...),
) -> list[SongResponse]:
    versions = await song_service.search(mode, q)
    return [SongResponse.from_entity(v) for v in versions]


@router.get('/browse', response_model=list[SongResponse])
async def browse_songs(
    song_service: Annotated[SongService, Depends(get_song_service)],
    _user: Annotated[User, Depends(get_current_active_user)],
    lang: str = Query(default=''),
    collection: str = Query(default=''),
    tonality: str = Query(default=''),
) -> list[SongResponse]:
    versions = await song_service.browse(lang=lang, collection=collection, tonality=tonality)
    return [SongResponse.from_entity(v) for v in versions]


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
