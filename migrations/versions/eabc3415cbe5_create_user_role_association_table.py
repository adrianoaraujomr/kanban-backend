"""create_user_role_association_table

Revision ID: eabc3415cbe5
Revises: 33ef3a044332
Create Date: 2025-04-10 03:21:07.833720

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'eabc3415cbe5'
down_revision: Union[str, None] = '33ef3a044332'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("user_roles",
                    sa.Column("id", sa.Integer(), nullable=False),
                    sa.Column("id_user", sa.Integer(), nullable=False),
                    sa.Column("id_role", sa.String(length=50), nullable=False),
                    sa.PrimaryKeyConstraint("id"),
                    sa.ForeignKeyConstraint(('id_user',), ["users.id"]),
                    sa.ForeignKeyConstraint(('id_role',), ["roles.id"])
                    )


def downgrade() -> None:
    op.drop_table("user_roles")
