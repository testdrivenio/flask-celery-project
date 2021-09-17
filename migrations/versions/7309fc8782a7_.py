"""empty message

Revision ID: 7309fc8782a7
Revises: 69fd8a9d569e
Create Date: 2021-09-17 01:42:45.564119

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7309fc8782a7'
down_revision = '69fd8a9d569e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('members',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('username', sa.String(length=128), nullable=False),
    sa.Column('email', sa.String(length=128), nullable=False),
    sa.Column('avatar', sa.String(length=256), nullable=False),
    sa.Column('avatar_thumbnail', sa.String(length=256), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('members')
    # ### end Alembic commands ###