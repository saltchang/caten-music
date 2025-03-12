from decouple import config

DATABASE_URL = config(
    'DATABASE_URL',
    default='postgresql://postgres:postgres@localhost:5432/postgres',
    cast=str,
)
