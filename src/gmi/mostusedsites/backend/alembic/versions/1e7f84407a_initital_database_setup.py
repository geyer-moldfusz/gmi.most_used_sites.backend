from alembic import op
import sqlalchemy as sa

"""initital database setup

Revision ID: 1e7f84407a
Revises:
Create Date: 2015-11-25 14:11:39.297090

"""

# revision identifiers, used by Alembic.
revision = '1e7f84407a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('unique_id', sa.String(length=24), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('unique_id'))
    op.create_table(
        'visits',
        sa.Column('id', sa.String(length=40), nullable=False),
        sa.Column('url', sa.String(length=512), nullable=False),
        sa.Column('scheme', sa.String(length=32), nullable=False),
        sa.Column('host', sa.String(length=512), nullable=False),
        sa.Column('path', sa.String(length=512), nullable=False),
        sa.Column('visited_at', sa.BigInteger(), nullable=False),
        sa.Column('duration', sa.Integer(), nullable=False),
        sa.Column('active', sa.Boolean(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id'))


def downgrade():
    op.drop_table('visits')
    op.drop_table('users')
