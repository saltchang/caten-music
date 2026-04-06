from app.core.validators import (
    check_login_format,
    validate_displayname,
    validate_email,
    validate_password,
    validate_username,
)


class TestValidateUsername:
    def test_valid_alphanumeric(self):
        """
        GIVEN a valid alphanumeric username
        WHEN validate_username is called
        THEN it should return True
        """
        # Act
        result = validate_username('testuser')

        # Assert
        assert result is True

    def test_valid_with_underscore_and_digits(self):
        """
        GIVEN a username containing underscores and digits
        WHEN validate_username is called
        THEN it should return True
        """
        # Act
        result = validate_username('Test_123')

        # Assert
        assert result is True

    def test_valid_minimum_length(self):
        """
        GIVEN a username at the minimum allowed length (4 characters)
        WHEN validate_username is called
        THEN it should return True
        """
        # Act
        result = validate_username('abcd')

        # Assert
        assert result is True

    def test_valid_maximum_length(self):
        """
        GIVEN a username at the maximum allowed length (25 characters)
        WHEN validate_username is called
        THEN it should return True
        """
        # Act
        result = validate_username('a' * 25)

        # Assert
        assert result is True

    def test_invalid_empty(self):
        """
        GIVEN an empty string as username
        WHEN validate_username is called
        THEN it should return False
        """
        # Act
        result = validate_username('')

        # Assert
        assert result is False

    def test_invalid_too_short(self):
        """
        GIVEN a username shorter than the minimum length
        WHEN validate_username is called
        THEN it should return False
        """
        # Act
        result = validate_username('ab')

        # Assert
        assert result is False

    def test_invalid_too_long(self):
        """
        GIVEN a username exceeding the maximum length (26 characters)
        WHEN validate_username is called
        THEN it should return False
        """
        # Act
        result = validate_username('a' * 26)

        # Assert
        assert result is False

    def test_invalid_with_spaces(self):
        """
        GIVEN a username containing spaces
        WHEN validate_username is called
        THEN it should return False
        """
        # Act
        result = validate_username('user name')

        # Assert
        assert result is False

    def test_invalid_with_special_chars(self):
        """
        GIVEN a username containing special characters
        WHEN validate_username is called
        THEN it should return False
        """
        # Act
        result = validate_username('user@name')

        # Assert
        assert result is False


class TestValidateEmail:
    def test_valid_simple(self):
        """
        GIVEN a valid simple email address
        WHEN validate_email is called
        THEN it should return True
        """
        # Act
        result = validate_email('test@example.com')

        # Assert
        assert result is True

    def test_valid_with_subdomain(self):
        """
        GIVEN an email address with a subdomain
        WHEN validate_email is called
        THEN it should return True
        """
        # Act
        result = validate_email('user@mail.example.com')

        # Assert
        assert result is True

    def test_valid_with_dots(self):
        """
        GIVEN an email address with dots in the local part
        WHEN validate_email is called
        THEN it should return True
        """
        # Act
        result = validate_email('first.last@example.com')

        # Assert
        assert result is True

    def test_invalid_empty(self):
        """
        GIVEN an empty string as email
        WHEN validate_email is called
        THEN it should return False
        """
        # Act
        result = validate_email('')

        # Assert
        assert result is False

    def test_invalid_no_at(self):
        """
        GIVEN an email string missing the @ symbol
        WHEN validate_email is called
        THEN it should return False
        """
        # Act
        result = validate_email('notanemail')

        # Assert
        assert result is False

    def test_invalid_no_domain(self):
        """
        GIVEN an email string missing the domain part
        WHEN validate_email is called
        THEN it should return False
        """
        # Act
        result = validate_email('user@')

        # Assert
        assert result is False


class TestValidatePassword:
    def test_valid_alphanumeric(self):
        """
        GIVEN a valid alphanumeric password
        WHEN validate_password is called
        THEN it should return True
        """
        # Act
        result = validate_password('TestPass1')

        # Assert
        assert result is True

    def test_valid_with_special_chars(self):
        """
        GIVEN a valid password with special characters
        WHEN validate_password is called
        THEN it should return True
        """
        # Act
        result = validate_password('p@ssW0rd!')

        # Assert
        assert result is True

    def test_valid_minimum_length(self):
        """
        GIVEN a password at the minimum allowed length (8 characters)
        WHEN validate_password is called
        THEN it should return True
        """
        # Act
        result = validate_password('abcdefgh')

        # Assert
        assert result is True

    def test_invalid_empty(self):
        """
        GIVEN an empty string as password
        WHEN validate_password is called
        THEN it should return False
        """
        # Act
        result = validate_password('')

        # Assert
        assert result is False

    def test_invalid_too_short(self):
        """
        GIVEN a password shorter than the minimum length
        WHEN validate_password is called
        THEN it should return False
        """
        # Act
        result = validate_password('short')

        # Assert
        assert result is False

    def test_invalid_with_spaces(self):
        """
        GIVEN a password containing spaces
        WHEN validate_password is called
        THEN it should return False
        """
        # Act
        result = validate_password('pass word 123')

        # Assert
        assert result is False


class TestValidateDisplayname:
    def test_valid_english(self):
        """
        GIVEN a valid English display name
        WHEN validate_displayname is called
        THEN it should return True
        """
        # Act
        result = validate_displayname('TestDisplay')

        # Assert
        assert result is True

    def test_valid_chinese(self):
        """
        GIVEN a valid Chinese display name within width limit
        WHEN validate_displayname is called
        THEN it should return True
        """
        # Act
        result = validate_displayname('測試名稱')

        # Assert
        assert result is True

    def test_valid_mixed(self):
        """
        GIVEN a valid display name mixing English and Chinese characters
        WHEN validate_displayname is called
        THEN it should return True
        """
        # Act
        result = validate_displayname('Salt鹽')

        # Assert
        assert result is True

    def test_invalid_empty(self):
        """
        GIVEN an empty string as display name
        WHEN validate_displayname is called
        THEN it should return False
        """
        # Act
        result = validate_displayname('')

        # Assert
        assert result is False

    def test_invalid_chinese_exceeding_width(self):
        """
        GIVEN a Chinese display name exceeding the width limit (9 chars = 18 width > 16)
        WHEN validate_displayname is called
        THEN it should return False
        """
        # Act
        result = validate_displayname('一二三四五六七八九')

        # Assert
        assert result is False

    def test_valid_chinese_at_width_limit(self):
        """
        GIVEN a Chinese display name at exactly the width limit (8 chars = 16 width)
        WHEN validate_displayname is called
        THEN it should return True
        """
        # Act
        result = validate_displayname('一二三四五六七八')

        # Assert
        assert result is True

    def test_invalid_with_spaces(self):
        """
        GIVEN a display name containing spaces
        WHEN validate_displayname is called
        THEN it should return False
        """
        # Act
        result = validate_displayname('test name')

        # Assert
        assert result is False


class TestCheckLoginFormat:
    def test_email_primary(self):
        """
        GIVEN a valid email as login primary and a valid password
        WHEN check_login_format is called
        THEN primary_type should be 'email' and password_valid should be True
        """
        # Act
        result = check_login_format('test@example.com', 'password123')

        # Assert
        assert result['primary_type'] == 'email'
        assert result['password_valid'] is True

    def test_username_primary(self):
        """
        GIVEN a valid username as login primary and a valid password
        WHEN check_login_format is called
        THEN primary_type should be 'username' and password_valid should be True
        """
        # Act
        result = check_login_format('testuser', 'password123')

        # Assert
        assert result['primary_type'] == 'username'
        assert result['password_valid'] is True

    def test_invalid_primary(self):
        """
        GIVEN an invalid login primary and a valid password
        WHEN check_login_format is called
        THEN primary_type should be None and password_valid should be True
        """
        # Act
        result = check_login_format('!!invalid!!', 'password123')

        # Assert
        assert result['primary_type'] is None
        assert result['password_valid'] is True

    def test_invalid_password(self):
        """
        GIVEN a valid username and an invalid (too short) password
        WHEN check_login_format is called
        THEN primary_type should be 'username' and password_valid should be False
        """
        # Act
        result = check_login_format('testuser', 'short')

        # Assert
        assert result['primary_type'] == 'username'
        assert result['password_valid'] is False
