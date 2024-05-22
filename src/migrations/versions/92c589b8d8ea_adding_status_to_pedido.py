"""Adding status to pedido

Revision ID: 92c589b8d8ea
Revises: 4baf83c6887b
Create Date: 2024-05-22 17:23:40.950389

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "92c589b8d8ea"
down_revision: Union[str, None] = "4baf83c6887b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "pedido",
        sa.Column("status", sa.String(1), nullable=False, server_default="e"),
    )
    pass


def downgrade() -> None:
    op.drop_column("pedido", "status")
