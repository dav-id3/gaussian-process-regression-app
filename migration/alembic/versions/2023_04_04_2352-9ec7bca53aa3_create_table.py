"""create_table

Revision ID: 9ec7bca53aa3
Revises: 
Create Date: 2023-04-04 23:52:01.542333

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "9ec7bca53aa3"
down_revision = None
branch_labels = None
depends_on = None

TABLE_NAME = "predicted_data"


def upgrade() -> None:
    # TBU for initial table creation on predicted next value
    op.create_table(
        TABLE_NAME,
        sa.Column("value", sa.Float, nullable=False),
        sa.Column("time", sa.String(length=15), primary_key=True),
        sa.Column("lower_bound", sa.Float, nullable=False),
        sa.Column("upper_bound", sa.Float, nullable=False),
    )


def downgrade() -> None:
    op.drop_table(TABLE_NAME)
