# Environment

Configuration is managed via `pydantic-settings` (`app/config/settings.py`). All values can be set through environment variables or a `.env` file.

## Required

```
DATABASE_URL=postgresql://user:pass@host:5432/db   # Auto-converted to postgresql+asyncpg://
SECRET_KEY=your-secret-key                         # HMAC-SHA256 signing for JWT tokens
HASH_SALT=your-hash-salt                           # SHA256 password hashing salt
CHURCH_MUSIC_API_URL=https://...                   # External church music API base URL
```

## Optional (with defaults)

```
APP_SETTING=Development                            # Development | Testing | Production
DEBUG=false
CONTACT_EMAIL=
DROPBOX_ACCESS_TOKEN=                              # For PPT/sheet file downloads

# JWT token expiry
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=20160              # 14 days
JWT_REFRESH_TOKEN_EXPIRE_MINUTES=43200             # 30 days
JWT_ACTIVATION_TOKEN_EXPIRE_MINUTES=120            # 2 hours

# SMTP (activation & password reset emails)
SMTP_HOST=smtp.mailgun.org
SMTP_PORT=465
SMTP_USERNAME=
SMTP_PASSWORD=
SMTP_USE_SSL=true
```
