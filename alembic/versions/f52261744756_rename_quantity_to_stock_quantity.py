"""rename quantity to stock_quantity

Revision ID: f52261744756
Revises: 2ddeedf556bd
Create Date: 2026-10-21 19:00:27.443153

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f52261744756'
down_revision: Union[str, Sequence[str], None] = '2ddeedf556bd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        "products",
        "quantity",
        new_column_name="stock_quantity",
        existing_type=sa.Integer(),
        existing_nullable=False,
    )


def downgrade() -> None:
    op.alter_column(
        "products",
        "stock_quantity",
        new_column_name="quantity",
        existing_type=sa.Integer(),
        existing_nullable=False,
    )
