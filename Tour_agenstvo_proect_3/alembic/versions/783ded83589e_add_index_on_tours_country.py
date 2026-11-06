"""add index on tours.country

Revision ID: 783ded83589e
Revises: fcfbaaaec337
Create Date: 2026-11-07 00:15:39.513492

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '783ded83589e'
down_revision: Union[str, Sequence[str], None] = 'fcfbaaaec337'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_index("ix_tours_country", "tours", ["country"])

def downgrade() -> None:
    op.drop_index("ix_tours_country", table_name="tours")