"""remove active col

Revision ID: 642e512218b9
Revises: 32a2def3b69a
Create Date: 2025-01-24 13:40:27.916195

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '642e512218b9'
down_revision = '32a2def3b69a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('active')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('active', sa.BOOLEAN(), autoincrement=False, nullable=True))

    # ### end Alembic commands ###
