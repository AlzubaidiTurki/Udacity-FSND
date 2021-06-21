"""empty message

Revision ID: 7432e67e97af
Revises: 86f1baa8f4ad
Create Date: 2021-06-18 15:34:16.777274

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7432e67e97af'
down_revision = '86f1baa8f4ad'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('venue', sa.Column('address', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('venue', 'address')
    # ### end Alembic commands ###
