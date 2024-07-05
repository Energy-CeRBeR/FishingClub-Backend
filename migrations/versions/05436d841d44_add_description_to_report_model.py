"""Add description to report model

Revision ID: 05436d841d44
Revises: 6fc74711b305
Create Date: 2024-07-05 09:59:25.316503

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '05436d841d44'
down_revision: Union[str, None] = '6fc74711b305'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('reports', sa.Column('description', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('reports', 'description')
    # ### end Alembic commands ###
