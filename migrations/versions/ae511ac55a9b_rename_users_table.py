"""Rename users table

Revision ID: ae511ac55a9b
Revises: 71d35a08f271
Create Date: 2026-07-15 23:54:17.997948

"""

from alembic import op

# revision identifiers, used by Alembic.
revision = "ae511ac55a9b"
down_revision = "71d35a08f271"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.rename_table("user", "users")


def downgrade() -> None:
    op.rename_table("users", "user")
