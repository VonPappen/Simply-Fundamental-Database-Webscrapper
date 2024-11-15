"""Security Model __str__

Revision ID: 7e16430b01b2
Revises: 9385c7a823ef
Create Date: 2021-09-14 18:08:44.893256

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7e16430b01b2'
down_revision = '9385c7a823ef'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index(op.f('ix_Balance_sheet_annual_date'), 'Balance_sheet_annual', ['date'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_Balance_sheet_annual_date'), table_name='Balance_sheet_annual')
    # ### end Alembic commands ###
