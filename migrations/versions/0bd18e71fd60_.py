"""empty message

Revision ID: 0bd18e71fd60
Revises: 132e4b7d1464
Create Date: 2016-10-11 10:57:48.447989

"""

# revision identifiers, used by Alembic.
revision = '0bd18e71fd60'
down_revision = '132e4b7d1464'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('market', 'time')
    op.drop_column('market', 'date')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('market', sa.Column('date', sa.DATE(), nullable=False))
    op.add_column('market', sa.Column('time', sa.TIME(), nullable=False))
    ### end Alembic commands ###
