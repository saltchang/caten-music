from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies import get_current_admin, get_current_manager, get_song_service, get_user_service
from app.api.schemas.song import SongCreateRequest, SongResponse, SongUpdateRequest
from app.api.schemas.user import UserResponse, UserUpdateRequest
from app.core.entities.user import User
from app.core.exceptions import InvalidInputError, UserNotFoundError
from app.service.song_service import SongService
from app.service.user_service import UserService

router = APIRouter(prefix='/admin', tags=['admin'])


@router.get('/users', response_model=list[UserResponse])
async def list_users(
    _admin: Annotated[User, Depends(get_current_admin)],
    user_service: Annotated[UserService, Depends(get_user_service)],
):
    users = await user_service.list_users()
    return [_user_to_response(u) for u in users]


@router.put('/users/{user_id}', response_model=UserResponse)
async def update_user(
    user_id: int,
    request: UserUpdateRequest,
    _admin: Annotated[User, Depends(get_current_admin)],
    user_service: Annotated[UserService, Depends(get_user_service)],
):
    try:
        user = await user_service.get_user(user_id)

        if request.role is not None:
            user = await user_service.update_user_role(user_id, request.role)

        if request.displayname is not None:
            user = await user_service.update_user_displayname(user_id, request.displayname)

        return _user_to_response(user)
    except UserNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found') from None
    except InvalidInputError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from None


@router.post('/songs', response_model=SongResponse, status_code=status.HTTP_201_CREATED)
async def create_song(
    request: SongCreateRequest,
    _manager: Annotated[User, Depends(get_current_manager)],
    song_service: Annotated[SongService, Depends(get_song_service)],
) -> SongResponse:
    created = await song_service.create_song(request.to_version_entity(), request.to_work_entity())
    return SongResponse.from_entity(created)


@router.put('/songs/{sid}', response_model=SongResponse)
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


@router.delete('/songs/{sid}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_song(
    sid: str,
    _manager: Annotated[User, Depends(get_current_manager)],
    song_service: Annotated[SongService, Depends(get_song_service)],
) -> None:
    success = await song_service.delete_song(sid)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Song not found')


def _user_to_response(user: User) -> UserResponse:
    return UserResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        displayname=user.displayname,
        is_admin=user.is_admin,
        is_manager=user.is_manager,
        is_active=user.is_active,
        is_authenticated=user.is_authenticated,
    )
