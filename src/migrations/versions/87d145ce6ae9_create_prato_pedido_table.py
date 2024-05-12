"""create pedido_pedido table

Revision ID: 87d145ce6ae9
Revises: 6f0a2b8e60d4
Create Date: 2024-05-12 01:46:01.678718

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '87d145ce6ae9'
down_revision: Union[str, None] = '6f0a2b8e60d4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'prato_pedido',
        sa.Column('id_prato', sa.Integer,
                  sa.ForeignKey('prato.id'), primary_key=True),
        sa.Column('id_pedido', sa.Integer,
                  sa.ForeignKey('pedido.id'), primary_key=True),
        sa.Column('quantidade_prato', sa.Integer, nullable=False),
        sa.Column('created_at', sa.DateTime())
    )


def downgrade() -> None:
    op.drop_table('prato_pedido')
