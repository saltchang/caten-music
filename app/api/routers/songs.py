from typing import Annotated, Any

from fastapi import APIRouter, Depends, Query

from app.api.dependencies import get_current_active_user, get_song_service, oauth2_scheme_optional
from app.core.entities.user import User
from app.service.song_service import SongService

router = APIRouter(prefix='/songs', tags=['songs'])


@router.get('/random')
async def get_random_songs(
    song_service: Annotated[SongService, Depends(get_song_service)],
    token: Annotated[str | None, Depends(oauth2_scheme_optional)] = None,
    amount: int = Query(default=6),
) -> list[dict[str, Any]]:
    if token is None:
        return []
    return await song_service.get_random(amount)


@router.get('/search')
async def search_songs(
    song_service: Annotated[SongService, Depends(get_song_service)],
    _user: Annotated[User, Depends(get_current_active_user)],
    mode: str = Query(...),
    q: str = Query(...),
) -> list[dict[str, Any]]:
    return await song_service.search(mode, q)


@router.get('/browse')
async def browse_songs(
    song_service: Annotated[SongService, Depends(get_song_service)],
    _user: Annotated[User, Depends(get_current_active_user)],
    lang: str = Query(default=''),
    collection: str = Query(default=''),
    tonality: str = Query(default=''),
) -> list[dict[str, Any]]:
    return await song_service.browse(lang=lang, collection=collection, tonality=tonality)


@router.get('/{sid}')
async def get_song(
    sid: str,
    song_service: Annotated[SongService, Depends(get_song_service)],
    _user: Annotated[User, Depends(get_current_active_user)],
) -> list[dict[str, Any]]:
    return await song_service.get_by_sid(sid)
