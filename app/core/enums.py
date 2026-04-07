from enum import StrEnum


class Language(StrEnum):
    """Supported song languages."""

    CHINESE = 'Chinese'
    TAIWANESE = 'Taiwanese'


class Tonality(StrEnum):
    """Musical keys for song versions."""

    C = 'C'
    Cm = 'Cm'
    C_SHARP = 'C#'
    D = 'D'
    Dm = 'Dm'
    Db = 'Db'
    E = 'E'
    Em = 'Em'
    Eb = 'Eb'
    F = 'F'
    Fm = 'Fm'
    F_SHARP_m = 'F#m'
    G = 'G'
    Gm = 'Gm'
    Gb = 'Gb'
    A = 'A'
    Am = 'Am'
    Ab = 'Ab'
    B = 'B'
    Bm = 'Bm'
    Bb = 'Bb'


class UserRole(StrEnum):
    """User role levels."""

    ADMIN = 'admin'
    MANAGER = 'manager'
    NORMAL = 'normal'
