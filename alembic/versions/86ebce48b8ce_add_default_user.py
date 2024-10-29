"""add default user

Revision ID: 86ebce48b8ce
Revises: 04b7c9c78886
Create Date: 2024-10-20 21:27:53.105720

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '86ebce48b8ce'
down_revision: Union[str, None] = '04b7c9c78886'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
        INSERT INTO usuario (id, nombre, email, tipo)
        VALUES (0, 'default', 'default@example.com', 'type3')
        ON CONFLICT (id) DO NOTHING;
        """
    )
    # ### end Alembic commands ###

def downgrade() -> None:

    op.execute(
        """
        DELETE FROM usuario WHERE id = 0 AND nombre = 'default';
        """
    )
    # ### end Alembic commands ###
