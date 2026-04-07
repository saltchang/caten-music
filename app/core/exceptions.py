class DomainError(Exception):
    pass


class InvalidCredentialsError(DomainError):
    pass


class UserNotActivatedError(DomainError):
    pass


class UserDeactivatedError(DomainError):
    pass


class UsernameExistsError(DomainError):
    pass


class EmailExistsError(DomainError):
    pass


class InvalidInputError(DomainError):
    pass


class InvitationCodeInvalidError(DomainError):
    pass


class InvitationCodeExpiredError(DomainError):
    pass


class InvitationCodeDisabledError(DomainError):
    pass


class SongNotFoundError(DomainError):
    pass


class SonglistNotFoundError(DomainError):
    pass


class UserNotFoundError(DomainError):
    pass


class PermissionDeniedError(DomainError):
    pass


class TokenInvalidError(DomainError):
    pass
