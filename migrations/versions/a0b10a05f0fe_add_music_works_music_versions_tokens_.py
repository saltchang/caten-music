"""add music_works and music_versions tables

Revision ID: a0b10a05f0fe
Revises: bcfc6041a78f
Create Date: 2026-04-06 22:54:45.094752

"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import ARRAY

# revision identifiers, used by Alembic.
revision = 'a0b10a05f0fe'
down_revision = 'bcfc6041a78f'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'music_works',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title_original', sa.String(length=255), nullable=False),
        sa.Column('composer', sa.String(length=255), nullable=True),
        sa.Column('lyricist', sa.String(length=255), nullable=True),
        sa.Column('scripture', sa.String(length=255), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        schema='public',
    )
    op.create_table(
        'music_versions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('work_id', sa.Integer(), nullable=False),
        sa.Column('sid', sa.String(length=7), nullable=False),
        sa.Column('num_c', sa.String(length=3), nullable=False),
        sa.Column('num_i', sa.String(length=3), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('language', sa.String(length=50), nullable=True),
        sa.Column('artist', sa.String(length=255), nullable=True),
        sa.Column('translator', sa.String(length=255), nullable=True),
        sa.Column('album', sa.String(length=255), nullable=True),
        sa.Column('tonality', sa.String(length=10), nullable=True),
        sa.Column('year', sa.String(length=10), nullable=True),
        sa.Column('lyrics', ARRAY(sa.Text()), nullable=True),
        sa.Column('tempo', sa.String(length=50), nullable=True),
        sa.Column('time_signature', sa.String(length=20), nullable=True),
        sa.Column('publisher', sa.String(length=255), nullable=True),
        sa.Column('publisher_original', sa.String(length=255), nullable=True),
        sa.ForeignKeyConstraint(['work_id'], ['public.music_works.id']),
        sa.PrimaryKeyConstraint('id'),
        schema='public',
    )
    op.create_index(
        op.f('ix_public_music_versions_sid'),
        'music_versions',
        ['sid'],
        unique=True,
        schema='public',
    )
    op.create_index(
        op.f('ix_public_music_versions_work_id'),
        'music_versions',
        ['work_id'],
        unique=False,
        schema='public',
    )


def downgrade():
    op.drop_index(
        op.f('ix_public_music_versions_work_id'),
        table_name='music_versions',
        schema='public',
    )
    op.drop_index(
        op.f('ix_public_music_versions_sid'),
        table_name='music_versions',
        schema='public',
    )
    op.drop_table('music_versions', schema='public')
    op.drop_table('music_works', schema='public')
