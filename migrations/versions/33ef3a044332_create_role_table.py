"""create_role_table

Revision ID: 33ef3a044332
Revises: 48b9b7400341
Create Date: 2025-04-10 03:16:35.838446

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '33ef3a044332'
down_revision: Union[str, None] = '48b9b7400341'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('roles',sa.Column('id', sa.String(length=50), nullable=False, unique=True),sa.PrimaryKeyConstraint("id"))


def downgrade() -> None:
    op.drop_table('roles')
