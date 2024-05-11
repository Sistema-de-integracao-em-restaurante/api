"""create prato table

Revision ID: 8911ec1c708e
Revises: f02dc2a616f8
Create Date: 2024-05-10 17:04:59.882347

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8911ec1c708e'
down_revision: Union[str, None] = 'f02dc2a616f8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'prato',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('nome', sa.String(50), nullable=False),
        sa.Column('preco', sa.Float),
        sa.Column('created_at', sa.DateTime())
    )


def downgrade() -> None:
    op.drop_table('prato')
