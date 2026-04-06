from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')

    # Database
    database_url: str = 'postgresql+asyncpg://postgres:postgres@localhost:5432/caten_music'

    # Auth
    secret_key: str = 'dev-secret-key'
    hash_salt: str = 'dev-hash-salt'
    jwt_algorithm: str = 'HS256'
    jwt_access_token_expire_minutes: int = 60 * 24 * 14  # 14 days
    jwt_refresh_token_expire_minutes: int = 60 * 24 * 30  # 30 days
    jwt_activation_token_expire_minutes: int = 120  # 2 hours

    # Dropbox
    dropbox_access_token: str = ''

    # SMTP
    smtp_host: str = 'smtp.mailgun.org'
    smtp_port: int = 465
    smtp_username: str = ''
    smtp_password: str = ''
    smtp_use_ssl: bool = True

    # App
    contact_email: str = ''
    app_setting: str = 'Development'
    debug: bool = False
    testing: bool = False

    @model_validator(mode='after')
    def ensure_async_database_url(self) -> Settings:
        if self.database_url.startswith('postgresql://'):
            self.database_url = self.database_url.replace('postgresql://', 'postgresql+asyncpg://', 1)
        return self
