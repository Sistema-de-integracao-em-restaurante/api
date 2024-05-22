"""create e ingrediente table

Revision ID: f02dc2a616f8
Revises:
Create Date: 2024-05-09 19:32:58.825395

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f02dc2a616f8'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'ingrediente',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('nome', sa.String(50), nullable=False),
        sa.Column('descricao', sa.Unicode(200)),
        sa.Column('created_at', sa.DateTime())
    )


def downgrade() -> None:
    op.drop_table('ingrediente')
