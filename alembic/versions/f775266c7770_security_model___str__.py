"""Security Model __str__

Revision ID: f775266c7770
Revises: a2c321cd8872
Create Date: 2021-09-14 18:04:32.992421

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'f775266c7770'
down_revision = 'a2c321cd8872'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Balance_sheet_annual',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('date', sa.Date(), nullable=False),
    sa.Column('statement', sa.String(), nullable=True),
    sa.Column('ticker', sa.String(), nullable=True),
    sa.Column('security_id', sa.Integer(), nullable=False),
    sa.Column('line_item', sa.String(), nullable=True),
    sa.Column('amount', postgresql.MONEY(), nullable=True),
    sa.ForeignKeyConstraint(['security_id'], ['Securities.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_Balance_sheet_annual_ticker'), 'Balance_sheet_annual', ['ticker'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_Balance_sheet_annual_ticker'), table_name='Balance_sheet_annual')
    op.drop_table('Balance_sheet_annual')
    # ### end Alembic commands ###
