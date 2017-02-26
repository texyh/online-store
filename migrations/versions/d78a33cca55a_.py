"""empty message

Revision ID: d78a33cca55a
Revises: 6713e3cfa637
Create Date: 2016-10-17 13:09:34.355455

"""

# revision identifiers, used by Alembic.
revision = 'd78a33cca55a'
down_revision = '6713e3cfa637'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('event', sa.Column('price', sa.String(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('event', 'price')
    ### end Alembic commands ###
