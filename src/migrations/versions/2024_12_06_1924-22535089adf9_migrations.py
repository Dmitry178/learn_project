"""migrations

Revision ID: 22535089adf9
Revises: 61cc23b0bb2d
Create Date: 2024-12-06 19:24:42.385875

"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "22535089adf9"
down_revision: Union[str, None] = "61cc23b0bb2d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint(
        "uq_room_facility", "rooms_facilities", ["room_id", "facility_id"]
    )


def downgrade() -> None:
    op.drop_constraint("uq_room_facility", "rooms_facilities", type_="unique")
