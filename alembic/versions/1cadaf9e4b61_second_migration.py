"""Second  migration

Revision ID: 1cadaf9e4b61
Revises: 09f787c97cfe
Create Date: 2024-10-12 14:59:13.973041

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1cadaf9e4b61'
down_revision: Union[str, None] = '09f787c97cfe'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('telegram_user',
    sa.Column('tg_id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=150), nullable=False),
    sa.Column('last_name', sa.String(length=150), nullable=True),
    sa.Column('username', sa.String(length=150), nullable=True),
    sa.Column('is_blocked', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('superuser', sa.Boolean(), nullable=True),
    sa.Column('staff_user', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('tg_id'),
    sa.UniqueConstraint('tg_id')
    )
    op.drop_table('user')
    op.add_column('file', sa.Column('created_by', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'file', 'telegram_user', ['created_by'], ['tg_id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'file', type_='foreignkey')
    op.drop_column('file', 'created_by')
    op.create_table('user',
    sa.Column('tg_id', sa.INTEGER(), nullable=False),
    sa.Column('username', sa.VARCHAR(), nullable=False),
    sa.Column('email', sa.VARCHAR(), nullable=False),
    sa.PrimaryKeyConstraint('tg_id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.drop_table('telegram_user')
    # ### end Alembic commands ###