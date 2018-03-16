"""empty message

Revision ID: bebc7baaa619
Revises: 
Create Date: 2018-03-16 01:16:03.000601

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bebc7baaa619'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('test_run', sa.Column('output', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('test_run', 'output')
    # ### end Alembic commands ###
