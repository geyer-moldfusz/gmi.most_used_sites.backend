"""deepcheck table

Revision ID: 56c52326119
Revises: 2e9e43b46d8
Create Date: 2016-01-13 14:19:04.936260

"""

# revision identifiers, used by Alembic.
revision = '56c52326119'
down_revision = '2e9e43b46d8'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    stats_table = op.create_table(
        'status',
        sa.Column('intact', sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint('intact'))
    op.bulk_insert(stats_table, [{'intact': True}])


def downgrade():
    op.drop_table('status')
