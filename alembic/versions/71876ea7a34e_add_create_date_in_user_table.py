"""add create date in user table

Revision ID: 71876ea7a34e
Revises: dd03c101d9a8
Create Date: 2022-04-24 16:55:17.833165

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '71876ea7a34e'
down_revision = 'dd03c101d9a8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'user',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('email', sa.String(length=120), nullable=False),
        sa.Column('hashed_password', sa.String(length=128), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('is_superuser', sa.Boolean(), nullable=True),
        sa.Column('channel', sa.String(length=20), nullable=True),
        sa.Column(
            'create_time', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False, comment='创建时间'
        ),
        sa.Column(
            'modified_time',
            sa.DateTime(),
            server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'),
            nullable=False
        ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    # ### end Alembic commands ###
