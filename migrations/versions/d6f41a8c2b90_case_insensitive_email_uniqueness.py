"""Make email addresses canonical and case-insensitively unique.

Revision ID: d6f41a8c2b90
Revises: 9f3c2a1b6d40
Create Date: 2026-11-11
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "d6f41a8c2b90"
down_revision: Union[str, Sequence[str], None] = "9f3c2a1b6d40"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Refuse to guess which account should survive if case variants already exist.
    op.execute(
        """
        DO $$
        BEGIN
            IF EXISTS (
                SELECT 1 FROM users
                GROUP BY lower(trim(email))
                HAVING count(*) > 1
            ) THEN
                RAISE EXCEPTION 'Cannot normalize emails: users contains addresses that differ only by case. Resolve those duplicate accounts, then rerun this migration.';
            END IF;
        END $$;
        """
    )
    op.drop_index("ix_users_email", table_name="users")
    op.execute("UPDATE users SET email = lower(trim(email))")
    op.create_index(
        "uq_users_email_lower", "users", [sa.text("lower(email)")], unique=True
    )


def downgrade() -> None:
    op.drop_index("uq_users_email_lower", table_name="users")
    op.create_index("ix_users_email", "users", ["email"], unique=True)
