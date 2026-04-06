from typing import Annotated, Any

from fastapi import APIRouter, Body, Depends, HTTPException, status

from app.api.dependencies import get_current_admin, get_current_manager, get_song_service, get_user_service
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


@router.post('/songs')
async def create_song(
    _manager: Annotated[User, Depends(get_current_manager)],
    song_service: Annotated[SongService, Depends(get_song_service)],
    data: Annotated[dict[str, Any], Body()],
) -> dict[str, Any]:
    new_sid = await song_service.create_song(data)
    return {'NewSID': new_sid}


@router.put('/songs/{sid}')
async def update_song(
    sid: str,
    _manager: Annotated[User, Depends(get_current_manager)],
    song_service: Annotated[SongService, Depends(get_song_service)],
    data: Annotated[dict[str, Any], Body()],
) -> dict[str, Any]:
    success = await song_service.update_song(sid, data)
    return {'success': success}


@router.delete('/songs/{sid}')
async def delete_song(
    sid: str,
    _manager: Annotated[User, Depends(get_current_manager)],
    song_service: Annotated[SongService, Depends(get_song_service)],
) -> dict[str, Any]:
    success = await song_service.delete_song(sid)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Song not found')
    return {'success': True}


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
