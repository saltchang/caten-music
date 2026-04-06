from collections.abc import AsyncGenerator
from functools import lru_cache
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.settings import Settings
from app.core.entities.user import User
from app.infrastructure.dropbox_client import DropboxFileService
from app.infrastructure.mail_service import SmtpMailService
from app.infrastructure.password_hasher import Sha256PasswordHasher
from app.infrastructure.song_api_client import HttpxSongApiClient
from app.infrastructure.token_service import JwtTokenService
from app.repository.database import get_session
from app.repository.invitation_repository import SqlAlchemyInvitationRepository
from app.repository.report_repository import SqlAlchemyReportRepository
from app.repository.songlist_repository import SqlAlchemySonglistRepository
from app.repository.user_profile_repository import SqlAlchemyUserProfileRepository
from app.repository.user_repository import SqlAlchemyUserRepository
from app.service.auth_service import AuthService
from app.service.file_service import FileService
from app.service.invitation_service import InvitationService
from app.service.report_service import ReportService
from app.service.song_service import SongService
from app.service.songlist_service import SonglistService
from app.service.user_service import UserService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/auth/login')
oauth2_scheme_optional = OAuth2PasswordBearer(tokenUrl='/api/auth/login', auto_error=False)


@lru_cache
def get_settings() -> Settings:
    return Settings()


async def get_db_session() -> AsyncGenerator[AsyncSession]:
    async for session in get_session():
        yield session


def get_password_hasher(
    settings: Annotated[Settings, Depends(get_settings)],
) -> Sha256PasswordHasher:
    return Sha256PasswordHasher(salt=settings.hash_salt)


def get_token_service(
    settings: Annotated[Settings, Depends(get_settings)],
) -> JwtTokenService:
    return JwtTokenService(
        secret_key=settings.secret_key,
        algorithm=settings.jwt_algorithm,
        access_token_expire_minutes=settings.jwt_access_token_expire_minutes,
        refresh_token_expire_minutes=settings.jwt_refresh_token_expire_minutes,
        activation_token_expire_minutes=settings.jwt_activation_token_expire_minutes,
    )


def get_user_repo(
    session: Annotated[AsyncSession, Depends(get_db_session)],
) -> SqlAlchemyUserRepository:
    return SqlAlchemyUserRepository(session)


def get_user_profile_repo(
    session: Annotated[AsyncSession, Depends(get_db_session)],
) -> SqlAlchemyUserProfileRepository:
    return SqlAlchemyUserProfileRepository(session)


def get_songlist_repo(
    session: Annotated[AsyncSession, Depends(get_db_session)],
) -> SqlAlchemySonglistRepository:
    return SqlAlchemySonglistRepository(session)


def get_invitation_repo(
    session: Annotated[AsyncSession, Depends(get_db_session)],
) -> SqlAlchemyInvitationRepository:
    return SqlAlchemyInvitationRepository(session)


def get_report_repo(
    session: Annotated[AsyncSession, Depends(get_db_session)],
) -> SqlAlchemyReportRepository:
    return SqlAlchemyReportRepository(session)


def get_song_api_client(
    settings: Annotated[Settings, Depends(get_settings)],
) -> HttpxSongApiClient:
    return HttpxSongApiClient(base_url=settings.church_music_api_url)


def get_file_service(
    settings: Annotated[Settings, Depends(get_settings)],
) -> DropboxFileService:
    return DropboxFileService(access_token=settings.dropbox_access_token)


def get_mail_service(
    settings: Annotated[Settings, Depends(get_settings)],
) -> SmtpMailService:
    return SmtpMailService(
        smtp_host=settings.smtp_host,
        smtp_port=settings.smtp_port,
        smtp_username=settings.smtp_username,
        smtp_password=settings.smtp_password,
        smtp_use_ssl=settings.smtp_use_ssl,
    )


def get_auth_service(
    user_repo: Annotated[SqlAlchemyUserRepository, Depends(get_user_repo)],
    user_profile_repo: Annotated[SqlAlchemyUserProfileRepository, Depends(get_user_profile_repo)],
    invitation_repo: Annotated[SqlAlchemyInvitationRepository, Depends(get_invitation_repo)],
    password_hasher: Annotated[Sha256PasswordHasher, Depends(get_password_hasher)],
    token_service: Annotated[JwtTokenService, Depends(get_token_service)],
    mail_service: Annotated[SmtpMailService, Depends(get_mail_service)],
) -> AuthService:
    return AuthService(
        user_repo=user_repo,
        user_profile_repo=user_profile_repo,
        invitation_repo=invitation_repo,
        password_hasher=password_hasher,
        token_service=token_service,
        mail_service=mail_service,
    )


def get_songlist_service(
    songlist_repo: Annotated[SqlAlchemySonglistRepository, Depends(get_songlist_repo)],
    song_api_client: Annotated[HttpxSongApiClient, Depends(get_song_api_client)],
) -> SonglistService:
    return SonglistService(songlist_repo=songlist_repo, song_api_client=song_api_client)


def get_invitation_service(
    invitation_repo: Annotated[SqlAlchemyInvitationRepository, Depends(get_invitation_repo)],
) -> InvitationService:
    return InvitationService(invitation_repo=invitation_repo)


def get_report_service(
    report_repo: Annotated[SqlAlchemyReportRepository, Depends(get_report_repo)],
) -> ReportService:
    return ReportService(report_repo=report_repo)


def get_user_service(
    user_repo: Annotated[SqlAlchemyUserRepository, Depends(get_user_repo)],
) -> UserService:
    return UserService(user_repo=user_repo)


def get_song_service(
    song_api_client: Annotated[HttpxSongApiClient, Depends(get_song_api_client)],
) -> SongService:
    return SongService(song_api_client=song_api_client)


def get_file_download_service(
    file_service: Annotated[DropboxFileService, Depends(get_file_service)],
) -> FileService:
    return FileService(file_service=file_service)


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    token_service: Annotated[JwtTokenService, Depends(get_token_service)],
    user_repo: Annotated[SqlAlchemyUserRepository, Depends(get_user_repo)],
) -> User:
    payload = token_service.decode_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid or expired token',
            headers={'WWW-Authenticate': 'Bearer'},
        )

    user = await user_repo.get_by_id(payload['sub'])
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='User not found',
            headers={'WWW-Authenticate': 'Bearer'},
        )

    return user


async def get_current_active_user(
    user: Annotated[User, Depends(get_current_user)],
) -> User:
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Account is deactivated',
        )
    return user


async def get_current_admin(
    user: Annotated[User, Depends(get_current_active_user)],
) -> User:
    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Admin privileges required',
        )
    return user


async def get_current_manager(
    user: Annotated[User, Depends(get_current_active_user)],
) -> User:
    if not user.is_manager:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Manager privileges required',
        )
    return user
