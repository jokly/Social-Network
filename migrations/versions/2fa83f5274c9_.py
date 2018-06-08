"""empty message

Revision ID: 2fa83f5274c9
Revises: 9412854bc4e1
Create Date: 2018-06-09 01:02:39.107015

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2fa83f5274c9'
down_revision = '9412854bc4e1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('external_social_network',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=256), nullable=True),
    sa.Column('url', sa.String(length=256), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name'),
    sa.UniqueConstraint('url')
    )
    op.create_table('access_token',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('token', sa.String(length=256), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('authorization_code',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('code', sa.String(length=256), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('external_social_network_session',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user', sa.Integer(), nullable=True),
    sa.Column('access_token', sa.String(length=256), nullable=True),
    sa.Column('ext_uid', sa.Integer(), nullable=True),
    sa.Column('ext_social_network', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['ext_social_network'], ['external_social_network.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('external_social_network_session')
    op.drop_table('authorization_code')
    op.drop_table('access_token')
    op.drop_table('external_social_network')
    # ### end Alembic commands ###
