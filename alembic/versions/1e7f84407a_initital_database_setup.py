"""initital database setup

Revision ID: 1e7f84407a
Revises: 
Create Date: 2015-11-25 14:11:39.297090

"""

### CAUTION! ###
# These migration is not the final one and may change for the production
# release. Do not roll out production setups based on this migration!

# revision identifiers, used by Alembic.
revision = '1e7f84407a'
down_revision = None
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('unique_id', sa.String(length=24), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('unique_id')
    )
    op.create_table('visits',
    sa.Column('id', sa.String(length=20), nullable=False),
    sa.Column('url', sa.String(length=512), nullable=False),
    sa.Column('scheme', sa.String(length=8), nullable=False),
    sa.Column('visited_at', sa.Integer(), nullable=False),
    sa.Column('duration', sa.Integer(), nullable=False),
    sa.Column('active', sa.Boolean(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('visits')
    op.drop_table('users')
