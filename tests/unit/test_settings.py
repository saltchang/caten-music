from app.config.settings import Settings


class TestSettings:
    def test_settings_with_defaults(self):
        """
        GIVEN required settings values (secret_key and hash_salt)
        WHEN a Settings instance is created without optional fields
        THEN it should use default values for jwt_algorithm and token expiry
        """
        # Arrange
        secret_key = 'test'
        hash_salt = 'salt'

        # Act
        settings = Settings(secret_key=secret_key, hash_salt=hash_salt)

        # Assert
        assert settings.secret_key == 'test'
        assert settings.hash_salt == 'salt'
        assert settings.jwt_algorithm == 'HS256'
        assert settings.jwt_access_token_expire_minutes == 60 * 24 * 14

    def test_database_url_auto_converts_to_asyncpg(self):
        """
        GIVEN a database_url using the plain postgresql:// scheme
        WHEN a Settings instance is created
        THEN the URL should be auto-converted to postgresql+asyncpg://
        """
        # Arrange
        db_url = 'postgresql://user:pass@localhost/db'

        # Act
        settings = Settings(
            database_url=db_url,
            secret_key='test',
            hash_salt='salt',
        )

        # Assert
        assert settings.database_url == 'postgresql+asyncpg://user:pass@localhost/db'

    def test_database_url_preserves_asyncpg_if_present(self):
        """
        GIVEN a database_url already using postgresql+asyncpg:// scheme
        WHEN a Settings instance is created
        THEN the URL should remain unchanged
        """
        # Arrange
        db_url = 'postgresql+asyncpg://user:pass@localhost/db'

        # Act
        settings = Settings(
            database_url=db_url,
            secret_key='test',
            hash_salt='salt',
        )

        # Assert
        assert settings.database_url == 'postgresql+asyncpg://user:pass@localhost/db'

    def test_sqlite_url_not_modified(self):
        """
        GIVEN a database_url using sqlite+aiosqlite:// scheme
        WHEN a Settings instance is created
        THEN the URL should remain unchanged
        """
        # Arrange
        db_url = 'sqlite+aiosqlite://'

        # Act
        settings = Settings(
            database_url=db_url,
            secret_key='test',
            hash_salt='salt',
        )

        # Assert
        assert settings.database_url == 'sqlite+aiosqlite://'
