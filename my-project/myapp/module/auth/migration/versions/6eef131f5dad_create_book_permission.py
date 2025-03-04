"""create_book_permission

Revision ID: 6eef131f5dad
Revises: 8ed025bcc845
Create Date: 2025-03-04 23:29:16.902059

"""

from typing import Sequence, Union

import sqlalchemy as sa
import sqlmodel  # 🔥 FastApp Modification
from alembic import op

from module.auth.migration_metadata import metadata

# revision identifiers, used by Alembic.
revision: str = "6eef131f5dad"
down_revision: Union[str, None] = "8ed025bcc845"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.bulk_insert(
        metadata.tables["permissions"],
        [
            {"name": "book:create", "description": "create book"},
            {"name": "book:read", "description": "read book"},
            {"name": "book:update", "description": "update book"},
            {"name": "book:delete", "description": "delete book"},
        ],
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    op.execute(
        sa.delete(metadata.tables["permissions"]).where(
            metadata.tables["permissions"].c.name.in_(
                "book:create",
                "book:read",
                "book:update",
                "book:delete",
            )
        )
    )
    # ### end Alembic commands ###
