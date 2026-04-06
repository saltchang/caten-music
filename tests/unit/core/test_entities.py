from datetime import datetime, timedelta

from app.core.entities.invitation_code import InvitationCode
from app.core.entities.song_report import SongReport
from app.core.entities.songlist import SongList
from app.core.entities.user import User
from app.core.entities.user_profile import UserProfile


class TestUserEntity:
    def test_creation(self):
        """
        GIVEN all fields including optional flags for a User entity
        WHEN a User is instantiated with explicit values
        THEN all attributes should match the provided values
        """
        # Act
        user = User(
            id=1,
            username='testuser',
            email='test@example.com',
            password_hash='abc123hash',
            displayname='TestUser',
            register_time=datetime(2024, 1, 1),
            is_authenticated=True,
            is_active=True,
            is_admin=False,
            is_manager=False,
        )

        # Assert
        assert user.id == 1
        assert user.username == 'testuser'
        assert user.email == 'test@example.com'
        assert user.displayname == 'TestUser'
        assert user.is_authenticated is True
        assert user.is_active is True
        assert user.is_admin is False

    def test_defaults(self):
        """
        GIVEN only required fields for a User entity
        WHEN a User is instantiated without optional flags
        THEN default values should be applied for all optional fields
        """
        # Act
        user = User(
            id=1,
            username='testuser',
            email='test@example.com',
            password_hash='abc123hash',
            displayname='TestUser',
        )

        # Assert
        assert user.is_authenticated is False
        assert user.is_active is True
        assert user.is_anonymous is False
        assert user.is_admin is False
        assert user.is_manager is False
        assert user.last_login_time is None


class TestUserProfileEntity:
    def test_creation(self):
        """
        GIVEN only required fields for a UserProfile entity
        WHEN a UserProfile is instantiated
        THEN optional fields should default to None
        """
        # Act
        profile = UserProfile(id=1, user_id=1)

        # Assert
        assert profile.id == 1
        assert profile.user_id == 1
        assert profile.about_me is None
        assert profile.phone_number is None
        assert profile.sex is None


class TestSongListEntity:
    def test_creation(self):
        """
        GIVEN all fields for a SongList entity
        WHEN a SongList is instantiated with explicit values
        THEN all attributes should match the provided values
        """
        # Act
        songlist = SongList(
            id=1,
            out_id='20240101001',
            title='My Songlist',
            user_id=1,
            songs_sid_list=['1001001', '1001002'],
            songs_amount=2,
        )

        # Assert
        assert songlist.id == 1
        assert songlist.title == 'My Songlist'
        assert songlist.songs_amount == 2
        assert len(songlist.songs_sid_list) == 2

    def test_defaults(self):
        """
        GIVEN only required fields for a SongList entity
        WHEN a SongList is instantiated without optional fields
        THEN default values should be applied for all optional fields
        """
        # Act
        songlist = SongList(id=1, user_id=1)

        # Assert
        assert songlist.out_id is None
        assert songlist.title is None
        assert songlist.description == ''
        assert songlist.songs_sid_list == []
        assert songlist.songs_amount == 0
        assert songlist.is_private is False
        assert songlist.is_archived is False

    def test_generate_out_id(self):
        """
        GIVEN a SongList with a known id and created_time
        WHEN generate_out_id is called
        THEN out_id should be formatted as YYYYMMDD + zero-padded id
        """
        # Arrange
        songlist = SongList(
            id=42,
            user_id=1,
            created_time=datetime(2024, 3, 15),
        )

        # Act
        songlist.generate_out_id()

        # Assert
        assert songlist.out_id == '20240315042'

    def test_generate_out_id_wraps_at_1000(self):
        """
        GIVEN a SongList with an id >= 1000
        WHEN generate_out_id is called
        THEN out_id should use id modulo 1000 (1234 % 1000 = 234)
        """
        # Arrange
        songlist = SongList(
            id=1234,
            user_id=1,
            created_time=datetime(2024, 3, 15),
        )

        # Act
        songlist.generate_out_id()

        # Assert
        assert songlist.out_id == '20240315234'

    def test_default_title_when_empty(self):
        """
        GIVEN a SongList with an empty title and a generated out_id
        WHEN set_default_title is called
        THEN the title should be set to the default pattern with the out_id

        NOTE: This test performs multiple sequential Acts (generate_out_id
        then set_default_title) because set_default_title depends on out_id.
        """
        # Arrange
        songlist = SongList(id=42, user_id=1, title='', created_time=datetime(2024, 3, 15))
        songlist.generate_out_id()

        # Act
        songlist.set_default_title()

        # Assert
        assert songlist.title == '未命名歌單-20240315042'


class TestInvitationCodeEntity:
    def test_is_valid_when_active_and_not_expired(self):
        """
        GIVEN an invitation code that is not disabled and not yet expired
        WHEN is_valid is called
        THEN it should return True
        """
        # Arrange
        code = InvitationCode(
            id=1,
            code='ABC123',
            created_by=1,
            expires_at=datetime.now() + timedelta(hours=24),
            is_disabled=False,
        )

        # Act
        result = code.is_valid()

        # Assert
        assert result is True

    def test_is_invalid_when_expired(self):
        """
        GIVEN an invitation code that has expired
        WHEN is_valid is called
        THEN it should return False
        """
        # Arrange
        code = InvitationCode(
            id=1,
            code='ABC123',
            created_by=1,
            expires_at=datetime.now() - timedelta(hours=1),
            is_disabled=False,
        )

        # Act
        result = code.is_valid()

        # Assert
        assert result is False

    def test_is_invalid_when_disabled(self):
        """
        GIVEN an invitation code that is disabled but not expired
        WHEN is_valid is called
        THEN it should return False
        """
        # Arrange
        code = InvitationCode(
            id=1,
            code='ABC123',
            created_by=1,
            expires_at=datetime.now() + timedelta(hours=24),
            is_disabled=True,
        )

        # Act
        result = code.is_valid()

        # Assert
        assert result is False


class TestSongReportEntity:
    def test_creation(self):
        """
        GIVEN all required fields for a SongReport entity
        WHEN a SongReport is instantiated
        THEN all attributes should match the provided values
        """
        # Act
        report = SongReport(
            id=1,
            description='Wrong lyrics',
            song_sid=1001001,
            user_id=1,
        )

        # Assert
        assert report.id == 1
        assert report.description == 'Wrong lyrics'
        assert report.song_sid == 1001001
