"""Allow users to omit their phone number

Revision ID: c14b8f2d7a61
Revises: ae511ac55a9b
Create Date: 2026-10-20

"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "c14b8f2d7a61"
down_revision: Union[str, Sequence[str], None] = "ae511ac55a9b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column("users", "phone_number", nullable=True)


def downgrade() -> None:
    op.alter_column("users", "phone_number", nullable=False)
