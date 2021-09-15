"""Security Model __str__

Revision ID: 420d898545aa
Revises: 171bc05be950
Create Date: 2021-09-14 18:48:17.805392

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '420d898545aa'
down_revision = '171bc05be950'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('balance_sheet_quarterly',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('date', sa.Date(), nullable=False),
    sa.Column('statement', sa.String(), nullable=True),
    sa.Column('ticker', sa.String(), nullable=True),
    sa.Column('security_id', sa.Integer(), nullable=False),
    sa.Column('line_item', sa.String(), nullable=True),
    sa.Column('amount', postgresql.MONEY(), nullable=True),
    sa.ForeignKeyConstraint(['security_id'], ['Securities.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('date', 'ticker', 'line_item', name='unique_entry_bsq')
    )
    op.create_index('combo_index_bsq', 'balance_sheet_quarterly', ['date', 'ticker', 'line_item'], unique=False)
    op.create_index(op.f('ix_balance_sheet_quarterly_date'), 'balance_sheet_quarterly', ['date'], unique=False)
    op.create_index(op.f('ix_balance_sheet_quarterly_ticker'), 'balance_sheet_quarterly', ['ticker'], unique=False)
    op.drop_index('combo_index', table_name='Balance_sheet_annual')
    op.drop_constraint('unique_entry', 'Balance_sheet_annual', type_='unique')
    op.create_index('combo_index_bsa', 'Balance_sheet_annual', ['date', 'ticker', 'line_item'], unique=False)
    op.create_unique_constraint('unique_entry_bsa', 'Balance_sheet_annual', ['date', 'ticker', 'line_item'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('unique_entry_bsa', 'Balance_sheet_annual', type_='unique')
    op.drop_index('combo_index_bsa', table_name='Balance_sheet_annual')
    op.create_unique_constraint('unique_entry', 'Balance_sheet_annual', ['date', 'ticker', 'line_item'])
    op.create_index('combo_index', 'Balance_sheet_annual', ['date', 'ticker', 'line_item'], unique=False)
    op.drop_index(op.f('ix_balance_sheet_quarterly_ticker'), table_name='balance_sheet_quarterly')
    op.drop_index(op.f('ix_balance_sheet_quarterly_date'), table_name='balance_sheet_quarterly')
    op.drop_index('combo_index_bsq', table_name='balance_sheet_quarterly')
    op.drop_table('balance_sheet_quarterly')
    # ### end Alembic commands ###
