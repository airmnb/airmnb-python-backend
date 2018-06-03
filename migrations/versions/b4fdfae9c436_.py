"""empty message

Revision ID: b4fdfae9c436
Revises: b333f100a27b
Create Date: 2018-06-03 10:09:24.316246

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'b4fdfae9c436'
down_revision = 'b333f100a27b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('activities', sa.Column('end_date', sa.DATE(), nullable=False))
    op.add_column('activities', sa.Column('end_time', postgresql.TIME(timezone=True), nullable=False))
    op.add_column('activities', sa.Column('start_date', sa.DATE(), nullable=False))
    op.add_column('activities', sa.Column('start_time', postgresql.TIME(timezone=True), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('activities', 'start_time')
    op.drop_column('activities', 'start_date')
    op.drop_column('activities', 'end_time')
    op.drop_column('activities', 'end_date')
    # ### end Alembic commands ###