"""change song_reports.song_sid from integer to varchar

Revision ID: 2a5f0772101d
Revises: a0b10a05f0fe
Create Date: 2026-04-07 23:02:03.734870

"""

from alembic import op

# revision identifiers, used by Alembic.
revision = '2a5f0772101d'
down_revision = 'a0b10a05f0fe'
branch_labels = None
depends_on = None


def upgrade():
    op.execute('ALTER TABLE public.song_reports ALTER COLUMN song_sid TYPE VARCHAR(7) USING song_sid::VARCHAR')


def downgrade():
    op.execute('ALTER TABLE public.song_reports ALTER COLUMN song_sid TYPE INTEGER USING song_sid::INTEGER')
