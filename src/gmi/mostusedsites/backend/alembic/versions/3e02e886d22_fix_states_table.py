from alembic import op
import sqlalchemy as sa

"""fix state table

Revision ID: 3e02e886d22
Revises: 56c52326119
Create Date: 2016-01-16 16:44:13.418026

"""

# revision identifiers, used by Alembic.
revision = '3e02e886d22'
down_revision = '56c52326119'
branch_labels = None
depends_on = None


def upgrade():
    op.rename_table('status', 'states')


def downgrade():
    op.rename_table('states', 'status')
