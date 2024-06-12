"""mudança id_animal

Revision ID: 6059236355bf
Revises: df5ca79732c2
Create Date: 2024-05-26 22:32:40.765087

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6059236355bf'
down_revision: Union[str, None] = 'df5ca79732c2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
