"""create_book_permission

Revision ID: ff9b1bfcd66e
Revises: 8ed025bcc845
Create Date: 2025-03-14 20:18:03.022072

"""

from typing import Sequence, Union

import sqlalchemy as sa
import sqlmodel  # 🔥 FastApp Modification
from alembic import op

from module.auth.migration_metadata import metadata

# revision identifiers, used by Alembic.
revision: str = "ff9b1bfcd66e"
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
