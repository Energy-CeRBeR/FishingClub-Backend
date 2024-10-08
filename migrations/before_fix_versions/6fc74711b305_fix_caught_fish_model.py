"""FIX caught_fish model

Revision ID: 6fc74711b305
Revises: 12a0dd7033c2
Create Date: 2024-07-05 09:39:09.353219

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6fc74711b305'
down_revision: Union[str, None] = '12a0dd7033c2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('caught_fish', sa.Column('total_weight', sa.Float(), nullable=False))
    op.add_column('caught_fish', sa.Column('total_count', sa.Integer(), nullable=False))
    op.drop_column('caught_fish', 'weight')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('caught_fish', sa.Column('weight', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=False))
    op.drop_column('caught_fish', 'total_count')
    op.drop_column('caught_fish', 'total_weight')
    # ### end Alembic commands ###
