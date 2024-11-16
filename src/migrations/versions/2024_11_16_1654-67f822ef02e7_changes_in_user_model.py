"""changes in user model

Revision ID: 67f822ef02e7
Revises: 8f4063a0eadd
Create Date: 2024-11-16 16:54:39.508865

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "67f822ef02e7"
down_revision: Union[str, None] = "8f4063a0eadd"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "users", "first_name", existing_type=sa.VARCHAR(length=100), nullable=True
    )
    op.alter_column(
        "users", "last_name", existing_type=sa.VARCHAR(length=200), nullable=True
    )
    op.alter_column(
        "users", "username", existing_type=sa.VARCHAR(length=50), nullable=True
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "users", "username", existing_type=sa.VARCHAR(length=50), nullable=False
    )
    op.alter_column(
        "users", "last_name", existing_type=sa.VARCHAR(length=200), nullable=False
    )
    op.alter_column(
        "users", "first_name", existing_type=sa.VARCHAR(length=100), nullable=False
    )
    # ### end Alembic commands ###
