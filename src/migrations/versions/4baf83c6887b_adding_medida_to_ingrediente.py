"""Adding medida to ingrediente

Revision ID: 4baf83c6887b
Revises: 87d145ce6ae9
Create Date: 2024-05-22 13:57:36.902712

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "4baf83c6887b"
down_revision: Union[str, None] = "87d145ce6ae9"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "ingrediente",
        sa.Column("medida", sa.String(50), nullable=True, server_default="g"),
    )
    pass


def downgrade() -> None:
    op.drop_column("ingrediente", "medida")
