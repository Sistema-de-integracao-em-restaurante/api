"""create e integracao table

Revision ID: ca7a4cdaafe9
Revises: 92c589b8d8ea
Create Date: 2024-05-22 22:13:15.300042

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "ca7a4cdaafe9"
down_revision: Union[str, None] = "92c589b8d8ea"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "integracao",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("url", sa.String(200), nullable=False),
        sa.Column("created_at", sa.DateTime()),
    )


def downgrade() -> None:
    op.drop_table("integracao")
