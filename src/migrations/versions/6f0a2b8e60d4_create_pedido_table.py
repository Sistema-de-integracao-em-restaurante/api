"""create pedido table

Revision ID: 6f0a2b8e60d4
Revises: edcd22f8a364
Create Date: 2024-05-12 01:35:04.807415

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "6f0a2b8e60d4"
down_revision: Union[str, None] = "edcd22f8a364"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "pedido",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("nome_cliente", sa.String(50), nullable=False),
        sa.Column("forma_pagamento", sa.String(50), nullable=False),
        sa.Column("created_at", sa.DateTime()),
    )


def downgrade() -> None:
    op.drop_table("pedido")
