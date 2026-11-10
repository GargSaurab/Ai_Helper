"""Rename user indexes to match the users table.

Revision ID: 9f3c2a1b6d40
Revises: c14b8f2d7a61
Create Date: 2026-11-03
"""

from alembic import op

# revision identifiers, used by Alembic.
revision = "9f3c2a1b6d40"
down_revision = "c14b8f2d7a61"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("ALTER INDEX ix_user_email RENAME TO ix_users_email")
    op.execute("ALTER INDEX ix_user_phone_number RENAME TO ix_users_phone_number")


def downgrade() -> None:
    op.execute("ALTER INDEX ix_users_phone_number RENAME TO ix_user_phone_number")
    op.execute("ALTER INDEX ix_users_email RENAME TO ix_user_email")
