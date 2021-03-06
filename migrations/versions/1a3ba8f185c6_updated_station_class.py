"""Updated station class

Revision ID: 1a3ba8f185c6
Revises: dcaa12878181
Create Date: 2020-12-09 11:36:19.558981

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1a3ba8f185c6'
down_revision = 'dcaa12878181'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('station', sa.Column('name', sa.String(length=64), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('station', 'name')
    # ### end Alembic commands ###
