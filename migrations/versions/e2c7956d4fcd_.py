"""empty message

Revision ID: e2c7956d4fcd
Revises: 
Create Date: 2023-10-15 05:08:41.085476

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e2c7956d4fcd'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('password', sa.String(length=80), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    # ### end Alembic commands ###
