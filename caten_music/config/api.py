from decouple import config

CHURCH_MUSIC_API_URL = config(
    'CHURCH_MUSIC_API_URL',
    cast=str,
)
