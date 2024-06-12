"""empty message

Revision ID: df5ca79732c2
Revises: 
Create Date: 2024-05-26 00:35:11.150210

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'df5ca79732c2'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Alter the status column to Boolean type
    op.alter_column('objetivos', 'status',
                    existing_type=sa.String(length=64),
                    type_=sa.Boolean(),
                    existing_nullable=True,
                    postgresql_using='status::boolean')

def downgrade() -> None:
    # Revert the status column to String type
    op.alter_column('objetivos', 'status',
                    existing_type=sa.Boolean(),
                    type_=sa.String(length=64),
                    existing_nullable=True,
                    postgresql_using='status::text')