"""Remove url

Revision ID: 2e9e43b46d8
Revises: 1e7f84407a
Create Date: 2015-12-08 17:47:37.531723

"""

# revision identifiers, used by Alembic.
revision = '2e9e43b46d8'
down_revision = '1e7f84407a'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    try:
        op.drop_column('visits', 'url')
    except sa.exc.OperationalError:
        with op.batch_alter_table('visits') as batch_op:
            batch_op.drop_column('url')


def downgrade():
    op.add_column('visits', sa.Column('url', sa.VARCHAR(length=512), nullable=False))
