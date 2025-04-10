"""create_admin_role_admin_user

Revision ID: e46c35d24df9
Revises: eabc3415cbe5
Create Date: 2025-04-10 14:19:23.085333

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e46c35d24df9'
down_revision: Union[str, None] = 'eabc3415cbe5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("INSERT INTO users VALUES (1, 'root', 'root@email.com', '2b64f2e3f9fee1942af9ff60d40aa5a719db33b8ba8dd4864bb4f11e25ca2bee00907de32a59429602336cac832c8f2eeff5177cc14c864dd116c8bf6ca5d9a9')")
    op.execute("INSERT INTO roles VALUES ('admin')")
    op.execute("INSERT INTO user_roles VALUES (1, 1, 'admin')")


def downgrade() -> None:
    op.execute("DELETE FROM user_roles WHERE id = 1")
    op.execute("DELETE FROM roles WHERE id = 'admin'")
    op.execute("DELETE FROM users WHERe id = 1")
