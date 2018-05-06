"""empty message

Revision ID: b74564cfb73f
Revises: 
Create Date: 2018-05-06 14:17:31.798066

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'b74564cfb73f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('images',
    sa.Column('image_id', postgresql.UUID(), server_default=sa.text('uuid_generate_v4()'), nullable=False),
    sa.Column('blob', postgresql.BYTEA(), nullable=False),
    sa.Column('mime', sa.TEXT(), nullable=True),
    sa.Column('filename', sa.TEXT(), nullable=True),
    sa.PrimaryKeyConstraint('image_id')
    )
    op.create_table('locations',
    sa.Column('location_id', postgresql.UUID(), server_default=sa.text('uuid_generate_v4()'), autoincrement=False, nullable=False),
    sa.Column('langitude', postgresql.DOUBLE_PRECISION(), nullable=False),
    sa.Column('latitude', postgresql.DOUBLE_PRECISION(), nullable=False),
    sa.Column('addr1', sa.TEXT(), nullable=False),
    sa.Column('addr2', sa.TEXT(), nullable=True),
    sa.Column('addr3', sa.TEXT(), nullable=True),
    sa.Column('city', sa.TEXT(), nullable=False),
    sa.Column('state', sa.TEXT(), nullable=False),
    sa.Column('country', sa.TEXT(), nullable=False),
    sa.Column('postcode', sa.TEXT(), nullable=True),
    sa.PrimaryKeyConstraint('location_id')
    )
    op.create_table('users',
    sa.Column('user_id', postgresql.UUID(), server_default=sa.text('uuid_generate_v4()'), autoincrement=False, nullable=False),
    sa.Column('email', sa.TEXT(), nullable=True),
    sa.Column('nick_name', sa.TEXT(), nullable=True),
    sa.Column('family_name', sa.TEXT(), nullable=True),
    sa.Column('given_name', sa.TEXT(), nullable=True),
    sa.Column('full_name', sa.TEXT(), nullable=True),
    sa.Column('gender', sa.TEXT(), nullable=True),
    sa.Column('dob', sa.DATE(), nullable=True),
    sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('user_id')
    )
    op.create_table('wechat_users',
    sa.Column('wechat_user_id', postgresql.UUID(), server_default=sa.text('uuid_generate_v4()'), autoincrement=False, nullable=False),
    sa.Column('open_id', sa.TEXT(), nullable=False),
    sa.Column('avartar_url', sa.TEXT(), nullable=True),
    sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('wechat_user_id')
    )
    op.create_table('activities',
    sa.Column('activity_id', postgresql.UUID(), server_default=sa.text('uuid_generate_v4()'), autoincrement=False, nullable=False),
    sa.Column('name', sa.TEXT(), nullable=False),
    sa.Column('description', sa.TEXT(), nullable=True),
    sa.Column('location_id', postgresql.UUID(), nullable=False),
    sa.ForeignKeyConstraint(['location_id'], ['locations.location_id'], ),
    sa.PrimaryKeyConstraint('activity_id')
    )
    op.create_table('babies',
    sa.Column('baby_id', postgresql.UUID(), server_default=sa.text('uuid_generate_v4()'), autoincrement=False, nullable=False),
    sa.Column('family_name', sa.TEXT(), nullable=True),
    sa.Column('given_name', sa.TEXT(), nullable=True),
    sa.Column('full_name', sa.TEXT(), nullable=True),
    sa.Column('gender', sa.TEXT(), nullable=True),
    sa.Column('dob', sa.DATE(), nullable=False),
    sa.Column('parent_id', postgresql.UUID(), nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['parent_id'], ['users.user_id'], ),
    sa.PrimaryKeyConstraint('baby_id')
    )
    op.create_table('sessions',
    sa.Column('session_id', postgresql.UUID(), server_default=sa.text('uuid_generate_v4()'), nullable=False),
    sa.Column('session_expires_at', postgresql.TIMESTAMP(timezone=True), nullable=False),
    sa.Column('user_id', postgresql.UUID(), nullable=True),
    sa.Column('access_token', sa.TEXT(), nullable=True),
    sa.Column('access_token_expires_at', postgresql.TIMESTAMP(timezone=True), nullable=True),
    sa.Column('refresh_token', sa.TEXT(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ),
    sa.PrimaryKeyConstraint('session_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('sessions')
    op.drop_table('babies')
    op.drop_table('activities')
    op.drop_table('wechat_users')
    op.drop_table('users')
    op.drop_table('locations')
    op.drop_table('images')
    # ### end Alembic commands ###