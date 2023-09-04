"""create_table

Revision ID: 9ec7bca53aa3
Revises: 
Create Date: 2023-04-04 23:52:01.542333

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "9ec7bca53aa3"
down_revision = None
branch_labels = None
depends_on = None

TABLE_NAME = "test"


def upgrade() -> None:
    # TBU for initial table creation on predicted next value
    op.create_table(
        TABLE_NAME,
        sa.Column("id", sa.Integer, primary_key=True, index=True, autoincrement=True),
        sa.Column("name", sa.String(length=15), nullable=False),
    )


def downgrade() -> None:
    op.drop_table(TABLE_NAME)
