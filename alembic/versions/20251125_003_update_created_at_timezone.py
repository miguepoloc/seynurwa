"""Update created_at to timestamp with timezone

Revision ID: 003
Revises: 002
Create Date: 2025-11-25

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers
revision: str = '003'
down_revision: Union[str, None] = '002'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Update created_at column to use timezone."""
    # Alter column to TIMESTAMP WITH TIME ZONE
    op.execute("""
        ALTER TABLE emotions 
        ALTER COLUMN created_at TYPE TIMESTAMP WITH TIME ZONE 
        USING created_at AT TIME ZONE 'UTC'
    """)


def downgrade() -> None:
    """Revert created_at to timestamp without timezone."""
    op.execute("""
        ALTER TABLE emotions 
        ALTER COLUMN created_at TYPE TIMESTAMP WITHOUT TIME ZONE
    """)
