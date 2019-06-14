"""empty message

Revision ID: 737048117cae
Revises: 6eb477268cf0
Create Date: 2019-06-07 15:17:28.986183

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '737048117cae'
down_revision = '6eb477268cf0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('songlists', sa.Column('out_id', sa.String(length=32), nullable=True))
    op.drop_constraint('songlists_list_id_key', 'songlists', type_='unique')
    op.create_unique_constraint(None, 'songlists', ['out_id'])
    op.drop_column('songlists', 'list_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('songlists', sa.Column('list_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'songlists', type_='unique')
    op.create_unique_constraint('songlists_list_id_key', 'songlists', ['list_id'])
    op.drop_column('songlists', 'out_id')
    # ### end Alembic commands ###