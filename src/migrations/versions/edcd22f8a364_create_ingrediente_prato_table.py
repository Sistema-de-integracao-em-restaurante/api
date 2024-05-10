"""create ingrediente_prato table

Revision ID: edcd22f8a364
Revises: 8911ec1c708e
Create Date: 2024-05-10 17:22:59.800650

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'edcd22f8a364'
down_revision: Union[str, None] = '8911ec1c708e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'ingrediente_prato',
        sa.Column('id_ingrediente', sa.Integer,
                  sa.ForeignKey('ingrediente.id'), primary_key=True),
        sa.Column('id_prato', sa.Integer,
                  sa.ForeignKey('prato.id'), primary_key=True),
        sa.Column('quantidade_ingrediente', sa.Integer, nullable=False),
        sa.Column('created_at', sa.DateTime())
    )


def downgrade() -> None:
    op.drop_table('ingrediente_prato')
