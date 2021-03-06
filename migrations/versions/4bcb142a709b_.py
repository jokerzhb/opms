"""empty message

Revision ID: 4bcb142a709b
Revises: e42837613422
Create Date: 2019-04-26 12:49:26.347777

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4bcb142a709b'
down_revision = 'e42837613422'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('upgrade_log',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=32), nullable=True),
    sa.Column('content', sa.String(length=1024), nullable=True),
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.Column('creator', sa.String(length=32), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_upgrade_log_create_time'), 'upgrade_log', ['create_time'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_upgrade_log_create_time'), table_name='upgrade_log')
    op.drop_table('upgrade_log')
    # ### end Alembic commands ###
