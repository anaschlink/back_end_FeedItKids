"""add alimentacao_saudavel column to status_animal

Revision ID: 51935c8fa10f
Revises: 6059236355bf
Create Date: 2024-05-29 09:04:59.765895

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '51935c8fa10f'
down_revision: Union[str, None] = '6059236355bf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index(op.f('ix_alimento_status_grupo_alimento'), 'alimento_status', ['grupo_alimento'], unique=False)
    op.add_column('status_animal', sa.Column('alimentacao_saudavel', sa.Float(), nullable=False))
    op.add_column('status_animal', sa.Column('energia', sa.Float(), nullable=False))
    op.add_column('status_animal', sa.Column('forca', sa.Float(), nullable=False))
    op.add_column('status_animal', sa.Column('resistencia', sa.Float(), nullable=False))
    op.add_column('status_animal', sa.Column('felicidade', sa.Float(), nullable=False))
    op.drop_constraint('status_animal_status_fkey', 'status_animal', type_='foreignkey')
    op.drop_column('status_animal', 'status')
    op.create_unique_constraint(None, 'usuarios', ['id_animal'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'usuarios', type_='unique')
    op.add_column('status_animal', sa.Column('status', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('status_animal_status_fkey', 'status_animal', 'alimento_status', ['status'], ['id_status_alimento'])
    op.drop_column('status_animal', 'felicidade')
    op.drop_column('status_animal', 'resistencia')
    op.drop_column('status_animal', 'forca')
    op.drop_column('status_animal', 'energia')
    op.drop_column('status_animal', 'alimentacao_saudavel')
    op.drop_index(op.f('ix_alimento_status_grupo_alimento'), table_name='alimento_status')
    # ### end Alembic commands ###
