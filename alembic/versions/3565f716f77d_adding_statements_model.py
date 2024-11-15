"""Adding statements model

Revision ID: 3565f716f77d
Revises: 9c85e9310439
Create Date: 2021-09-15 22:54:01.136959

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3565f716f77d'
down_revision = '9c85e9310439'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('statements_table_log', sa.Column('days_after_release', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('statements_table_log', 'days_after_release')
    # ### end Alembic commands ###
