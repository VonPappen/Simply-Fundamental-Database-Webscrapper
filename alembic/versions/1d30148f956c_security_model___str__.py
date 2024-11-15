"""Security Model __str__

Revision ID: 1d30148f956c
Revises: 7e16430b01b2
Create Date: 2021-09-14 18:11:08.316443

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1d30148f956c'
down_revision = '7e16430b01b2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index('combo_index', 'Balance_sheet_annual', ['date', 'ticker', 'line_item'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('combo_index', table_name='Balance_sheet_annual')
    # ### end Alembic commands ###
