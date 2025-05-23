"""upgrade bookings 3

Revision ID: 7c16c5b7d605
Revises: 563e24c0e65e
Create Date: 2025-04-09 03:58:36.037315

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "7c16c5b7d605"
down_revision: Union[str, None] = "563e24c0e65e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "bookings", sa.Column("created_at", sa.DateTime(), nullable=False)
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("bookings", "created_at")
    # ### end Alembic commands ###
