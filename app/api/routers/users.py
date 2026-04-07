from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies import get_current_admin, get_user_service
from app.api.schemas.user import UserResponse, UserUpdateRequest
from app.core.entities.user import User
from app.core.exceptions import InvalidInputError, UserNotFoundError
from app.service.user_service import UserService

router = APIRouter(prefix='/users', tags=['users'])


@router.get('', response_model=list[UserResponse])
async def list_users(
    _admin: Annotated[User, Depends(get_current_admin)],
    user_service: Annotated[UserService, Depends(get_user_service)],
):
    users = await user_service.list_users()
    return [UserResponse.from_entity(u) for u in users]


@router.put('/{user_id}', response_model=UserResponse)
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

        return UserResponse.from_entity(user)
    except UserNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found') from None
    except InvalidInputError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from None
