"""Create Posts Table

Revision ID: e13ea36d1a3d
Revises: 
Create Date: 2024-03-24 16:17:15.724316

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e13ea36d1a3d'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("posts",
                    sa.Column("id",sa.Integer(),nullable=False,primary_key=True),
                    sa.Column("title",sa.String(),nullable=False,)

                    )
    pass


def downgrade() -> None:
    op.drop_table("posts")
    pass
