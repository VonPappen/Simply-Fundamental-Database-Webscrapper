"""Security Model __str__

Revision ID: 57ae6623d141
Revises: 6622044721cf
Create Date: 2021-09-14 18:45:20.145279

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '57ae6623d141'
down_revision = '6622044721cf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('unique_entry', 'Balance_sheet_annual', ['date', 'ticker', 'line_item'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('unique_entry', 'Balance_sheet_annual', type_='unique')
    # ### end Alembic commands ###
