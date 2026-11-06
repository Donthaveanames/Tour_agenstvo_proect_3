"""add trgm index tours.country

Revision ID: c1bf1290e22c
Revises: ba13fcfa6c57
Create Date: 2026-11-07 01:35:12.672624

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c1bf1290e22c'
down_revision: Union[str, Sequence[str], None] = 'ba13fcfa6c57'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm")
    op.execute(
        "CREATE INDEX ix_tours_country_trgm "
        "ON tours USING gin (country gin_trgm_ops)"
    )

def downgrade() -> None:
    op.execute("DROP INDEX IF EXISTS ix_tours_country_trgm")