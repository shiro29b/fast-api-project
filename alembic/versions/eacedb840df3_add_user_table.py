"""add user table

Revision ID: eacedb840df3
Revises: dd58375f57b9
Create Date: 2024-03-31 01:11:04.203143

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'eacedb840df3'
down_revision: Union[str, None] = 'dd58375f57b9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("users",
                     sa.Column("id",sa.Integer(),nullable=False),
                     sa.Column("email",sa.String(),nullable=False,),
                     sa.Column("password",sa.String(),nullable=False),
                     sa.Column("created_at", sa.TIMESTAMP(timezone=True),server_default=sa.text("now()"),nullable=False),
                     sa.PrimaryKeyConstraint("id"),
                     sa.UniqueConstraint("email")
                     )
    pass


def downgrade() -> None:
    op.drop_table("users")
    pass
