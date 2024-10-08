"""Add new columns in user model

Revision ID: 12a47c8cad9b
Revises: a96aa603d2bf
Create Date: 2024-08-20 19:17:56.034229

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '12a47c8cad9b'
down_revision: Union[str, None] = 'a96aa603d2bf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('is_active', sa.Boolean(), nullable=False))
    op.add_column('users', sa.Column('is_admin', sa.Boolean(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'is_admin')
    op.drop_column('users', 'is_active')
    # ### end Alembic commands ###
