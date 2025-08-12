"""generate test data

Revision ID: 1d3df9f24e3b
Revises: 64023d1ee1aa
Create Date: 2025-08-11 17:02:36.390230

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from app.config.security import hash_password
from app.services.account import generate_account_number

# revision identifiers, used by Alembic.
revision: str = '1d3df9f24e3b'
down_revision: Union[str, Sequence[str], None] = '64023d1ee1aa'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    conn = op.get_bind()

    user_result = conn.execute(
        sa.text(
            """
            INSERT INTO users (full_name, email, is_admin, password)
            VALUES (:full_name1, :email1, :is_admin1, :password1),
                   (:full_name2, :email2, :is_admin2, :password2)
            RETURNING id
            """
        ),
        {
            "full_name1": "test user",
            "email1": "testuser@test.com",
            "is_admin1": False,
            "password1": hash_password("testuserpassword"),

            "full_name2": "test admin",
            "email2": "testadmin@test.com",
            "is_admin2": True,
            "password2": hash_password("testadminpassword"),
        }
    ).fetchall()

    user_ids = [row[0] for row in user_result]

    for user_id, balance in zip(user_ids, [100, 200]):
        conn.execute(
            sa.text(
                """
                INSERT INTO accounts (account_number, balance, user_id)
                VALUES (:account_number, :balance, :user_id)
                """
            ),
            {
                "account_number": generate_account_number(),
                "balance": balance,
                "user_id": user_id,
            }
        )


def downgrade() -> None:
    """Downgrade schema."""
    conn = op.get_bind()
    conn.execute(
        sa.text(
            "DELETE FROM accounts WHERE user_id IN (SELECT id FROM users WHERE email IN ('testuser@test.com', 'testadmin@test.com'))"
        )
    )
    conn.execute(
        sa.text(
            "DELETE FROM users WHERE email IN ('testuser@test.com', 'testadmin@test.com')"
        )
    )
