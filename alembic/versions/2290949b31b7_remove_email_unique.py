"""remove email unique

Revision ID: 2290949b31b7
Revises: dda18f29ab71
Create Date: 2023-01-06 18:50:34.048378

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2290949b31b7'
down_revision = 'dda18f29ab71'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_users_email', table_name='users')
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.create_index('ix_users_email', 'users', ['email'], unique=False)
    # ### end Alembic commands ###
