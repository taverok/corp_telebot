"""empty message

Revision ID: 9027e700b82d
Revises: a15b2da11306
Create Date: 2019-04-16 12:11:45.365638

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9027e700b82d'
down_revision = 'a15b2da11306'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('token',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('code', sa.String(length=255), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('token')
    # ### end Alembic commands ###
