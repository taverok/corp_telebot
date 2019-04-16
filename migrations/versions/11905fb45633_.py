"""empty message

Revision ID: 11905fb45633
Revises: 
Create Date: 2019-04-16 14:00:29.539606

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '11905fb45633'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('document',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=255), nullable=False),
    sa.Column('icon', sa.Binary(), nullable=True),
    sa.Column('content', sa.UnicodeText(length=65000), nullable=True),
    sa.Column('is_private', sa.Boolean(), nullable=True),
    sa.Column('is_visible', sa.Boolean(), nullable=True),
    sa.Column('user_id', sa.BigInteger(), nullable=True),
    sa.Column('order_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('parent_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['parent_id'], ['document.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('title')
    )
    op.create_table('token',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('code', sa.String(length=255), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('telegram_id', sa.BigInteger(), nullable=True),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('surname', sa.String(length=255), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('role', sa.Enum('USER', 'ADMIN', 'SUPERADMIN', name='role'), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    op.drop_table('token')
    op.drop_table('document')
    # ### end Alembic commands ###