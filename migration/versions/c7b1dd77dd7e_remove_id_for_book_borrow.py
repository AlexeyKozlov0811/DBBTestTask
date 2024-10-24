"""remove_id_for_book_borrow

Revision ID: c7b1dd77dd7e
Revises: 0b7f99b782b6
Create Date: 2024-10-20 18:48:10.052728

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "c7b1dd77dd7e"
down_revision: str | None = "0b7f99b782b6"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("bookborrow", schema=None) as batch_op:
        batch_op.drop_column("id")

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("bookborrow", schema=None) as batch_op:
        batch_op.add_column(sa.Column("id", sa.INTEGER(), nullable=False))

    # ### end Alembic commands ###
