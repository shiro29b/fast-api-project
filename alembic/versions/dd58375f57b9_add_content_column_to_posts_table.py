"""add content column to posts table

Revision ID: dd58375f57b9
Revises: e13ea36d1a3d
Create Date: 2024-03-31 01:06:11.609198

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dd58375f57b9'
down_revision: Union[str, None] = 'e13ea36d1a3d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts",sa.Column("content", sa.String(),nullable= False))
    pass


def downgrade() -> None:
    op.drop_column("posts","content")
    pass
