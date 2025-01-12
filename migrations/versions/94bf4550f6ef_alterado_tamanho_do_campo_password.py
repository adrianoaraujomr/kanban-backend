"""Alterado tamanho do campo password

Revision ID: 94bf4550f6ef
Revises: 018cff04ff8f
Create Date: 2025-01-11 19:19:04.002105

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '94bf4550f6ef'
down_revision: Union[str, None] = '018cff04ff8f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'password', type_=sa.VARCHAR(250))
    op.alter_column('users', 'avatar', type_=sa.VARCHAR(250))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'avatar', type_=sa.VARCHAR(50))
    op.alter_column('users', 'password', type_=sa.VARCHAR(50))
    # ### end Alembic commands ###
