"""add orders and order_items tables

Revision ID: 6e9afb6286ca
Revises: c2bda800297a
Create Date: 2025-12-24 12:25:44.722639

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6e9afb6286ca'
down_revision: Union[str, Sequence[str], None] = 'c2bda800297a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
