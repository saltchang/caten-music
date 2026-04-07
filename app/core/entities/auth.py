from dataclasses import dataclass


@dataclass
class TokenPair:
    """Domain entity representing an access/refresh token pair."""

    access_token: str
    refresh_token: str


@dataclass
class AvailabilityResult:
    """Domain entity representing username/email availability check results."""

    username_taken: bool | None = None
    email_taken: bool | None = None
