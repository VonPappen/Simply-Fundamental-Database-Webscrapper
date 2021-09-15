"""adding tables final

Revision ID: 802aa834df11
Revises: 001f710e7f01
Create Date: 2021-09-14 19:25:37.858230

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '802aa834df11'
down_revision = '001f710e7f01'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('securities_table',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('ticker', sa.String(), nullable=True),
    sa.Column('company', sa.String(), nullable=True),
    sa.Column('sector', sa.String(), nullable=True),
    sa.Column('industry', sa.String(), nullable=True),
    sa.Column('country', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_securities_table_ticker'), 'securities_table', ['ticker'], unique=False)
    op.create_table('balance_sheet_annual',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('date', sa.Date(), nullable=False),
    sa.Column('statement', sa.String(), nullable=True),
    sa.Column('ticker', sa.String(), nullable=True),
    sa.Column('security_id', sa.Integer(), nullable=False),
    sa.Column('line_item', sa.String(), nullable=True),
    sa.Column('amount', postgresql.MONEY(), nullable=True),
    sa.ForeignKeyConstraint(['security_id'], ['securities_table.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('date', 'ticker', 'line_item', name='unique_entry_bsa')
    )
    op.create_index('combo_index_bsa', 'balance_sheet_annual', ['date', 'ticker', 'line_item'], unique=False)
    op.create_index(op.f('ix_balance_sheet_annual_date'), 'balance_sheet_annual', ['date'], unique=False)
    op.create_index(op.f('ix_balance_sheet_annual_ticker'), 'balance_sheet_annual', ['ticker'], unique=False)
    op.create_table('balance_sheet_quarterly',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('date', sa.Date(), nullable=False),
    sa.Column('statement', sa.String(), nullable=True),
    sa.Column('ticker', sa.String(), nullable=True),
    sa.Column('security_id', sa.Integer(), nullable=False),
    sa.Column('line_item', sa.String(), nullable=True),
    sa.Column('amount', postgresql.MONEY(), nullable=True),
    sa.ForeignKeyConstraint(['security_id'], ['securities_table.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('combo_index_bsq', 'balance_sheet_quarterly', ['date', 'ticker', 'line_item'], unique=False)
    op.create_index(op.f('ix_balance_sheet_quarterly_date'), 'balance_sheet_quarterly', ['date'], unique=False)
    op.create_index(op.f('ix_balance_sheet_quarterly_ticker'), 'balance_sheet_quarterly', ['ticker'], unique=False)
    op.create_table('cash_flow_statement_annual',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('date', sa.Date(), nullable=False),
    sa.Column('statement', sa.String(), nullable=True),
    sa.Column('ticker', sa.String(), nullable=True),
    sa.Column('security_id', sa.Integer(), nullable=False),
    sa.Column('line_item', sa.String(), nullable=True),
    sa.Column('amount', postgresql.MONEY(), nullable=True),
    sa.ForeignKeyConstraint(['security_id'], ['securities_table.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('date', 'ticker', 'line_item', name='unique_entry_cfa')
    )
    op.create_index(op.f('ix_cash_flow_statement_annual_date'), 'cash_flow_statement_annual', ['date'], unique=False)
    op.create_index(op.f('ix_cash_flow_statement_annual_ticker'), 'cash_flow_statement_annual', ['ticker'], unique=False)
    op.create_table('cash_flow_statement_quarterly',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('date', sa.Date(), nullable=False),
    sa.Column('statement', sa.String(), nullable=True),
    sa.Column('ticker', sa.String(), nullable=True),
    sa.Column('security_id', sa.Integer(), nullable=False),
    sa.Column('line_item', sa.String(), nullable=True),
    sa.Column('amount', postgresql.MONEY(), nullable=True),
    sa.ForeignKeyConstraint(['security_id'], ['securities_table.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('date', 'ticker', 'line_item', name='unique_entry_cfq')
    )
    op.create_index(op.f('ix_cash_flow_statement_quarterly_date'), 'cash_flow_statement_quarterly', ['date'], unique=False)
    op.create_index(op.f('ix_cash_flow_statement_quarterly_ticker'), 'cash_flow_statement_quarterly', ['ticker'], unique=False)
    op.create_table('financial_ratios_annual',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('date', sa.Date(), nullable=False),
    sa.Column('statement', sa.String(), nullable=True),
    sa.Column('ticker', sa.String(), nullable=True),
    sa.Column('security_id', sa.Integer(), nullable=False),
    sa.Column('line_item', sa.String(), nullable=True),
    sa.Column('amount', postgresql.MONEY(), nullable=True),
    sa.ForeignKeyConstraint(['security_id'], ['securities_table.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('date', 'ticker', 'line_item', name='unique_entry_fra')
    )
    op.create_index(op.f('ix_financial_ratios_annual_date'), 'financial_ratios_annual', ['date'], unique=False)
    op.create_index(op.f('ix_financial_ratios_annual_ticker'), 'financial_ratios_annual', ['ticker'], unique=False)
    op.create_table('financial_ratios_quarterly',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('date', sa.Date(), nullable=False),
    sa.Column('statement', sa.String(), nullable=True),
    sa.Column('ticker', sa.String(), nullable=True),
    sa.Column('security_id', sa.Integer(), nullable=False),
    sa.Column('line_item', sa.String(), nullable=True),
    sa.Column('amount', postgresql.MONEY(), nullable=True),
    sa.ForeignKeyConstraint(['security_id'], ['securities_table.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('date', 'ticker', 'line_item', name='unique_entry_frq')
    )
    op.create_index(op.f('ix_financial_ratios_quarterly_date'), 'financial_ratios_quarterly', ['date'], unique=False)
    op.create_index(op.f('ix_financial_ratios_quarterly_ticker'), 'financial_ratios_quarterly', ['ticker'], unique=False)
    op.create_table('income_statement_annual',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('date', sa.Date(), nullable=False),
    sa.Column('statement', sa.String(), nullable=True),
    sa.Column('ticker', sa.String(), nullable=True),
    sa.Column('security_id', sa.Integer(), nullable=False),
    sa.Column('line_item', sa.String(), nullable=True),
    sa.Column('amount', postgresql.MONEY(), nullable=True),
    sa.ForeignKeyConstraint(['security_id'], ['securities_table.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('date', 'ticker', 'line_item', name='unique_entry_isa')
    )
    op.create_index('combo_index_cfa', 'income_statement_annual', ['date', 'ticker', 'line_item'], unique=False)
    op.create_index('combo_index_fra', 'income_statement_annual', ['date', 'ticker', 'line_item'], unique=False)
    op.create_index('combo_index_isa', 'income_statement_annual', ['date', 'ticker', 'line_item'], unique=False)
    op.create_index(op.f('ix_income_statement_annual_date'), 'income_statement_annual', ['date'], unique=False)
    op.create_index(op.f('ix_income_statement_annual_ticker'), 'income_statement_annual', ['ticker'], unique=False)
    op.create_table('income_statement_quarterly',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('date', sa.Date(), nullable=False),
    sa.Column('statement', sa.String(), nullable=True),
    sa.Column('ticker', sa.String(), nullable=True),
    sa.Column('security_id', sa.Integer(), nullable=False),
    sa.Column('line_item', sa.String(), nullable=True),
    sa.Column('amount', postgresql.MONEY(), nullable=True),
    sa.ForeignKeyConstraint(['security_id'], ['securities_table.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('date', 'ticker', 'line_item', name='unique_entry_isq')
    )
    op.create_index('combo_index_cfq', 'income_statement_quarterly', ['date', 'ticker', 'line_item'], unique=False)
    op.create_index('combo_index_frq', 'income_statement_quarterly', ['date', 'ticker', 'line_item'], unique=False)
    op.create_index('combo_index_isq', 'income_statement_quarterly', ['date', 'ticker', 'line_item'], unique=False)
    op.create_index(op.f('ix_income_statement_quarterly_date'), 'income_statement_quarterly', ['date'], unique=False)
    op.create_index(op.f('ix_income_statement_quarterly_ticker'), 'income_statement_quarterly', ['ticker'], unique=False)
    op.drop_index('combo_index_bsa', table_name='Balance_sheet_annual')
    op.drop_index('ix_Balance_sheet_annual_date', table_name='Balance_sheet_annual')
    op.drop_index('ix_Balance_sheet_annual_ticker', table_name='Balance_sheet_annual')
    op.drop_table('Balance_sheet_annual')
    op.drop_index('combo_index_bsq', table_name='Balance_sheet_quarterly')
    op.drop_index('ix_Balance_sheet_quarterly_date', table_name='Balance_sheet_quarterly')
    op.drop_index('ix_Balance_sheet_quarterly_ticker', table_name='Balance_sheet_quarterly')
    op.drop_table('Balance_sheet_quarterly')
    op.drop_index('ix_Cash_flow_statement_quarterly_date', table_name='Cash_flow_statement_quarterly')
    op.drop_index('ix_Cash_flow_statement_quarterly_ticker', table_name='Cash_flow_statement_quarterly')
    op.drop_table('Cash_flow_statement_quarterly')
    op.drop_index('combo_index_cfq', table_name='Income_statement_quarterly')
    op.drop_index('combo_index_isq', table_name='Income_statement_quarterly')
    op.drop_index('ix_Income_statement_quarterly_date', table_name='Income_statement_quarterly')
    op.drop_index('ix_Income_statement_quarterly_ticker', table_name='Income_statement_quarterly')
    op.drop_table('Income_statement_quarterly')
    op.drop_index('ix_Cash_flow_statement_annual_date', table_name='Cash_flow_statement_annual')
    op.drop_index('ix_Cash_flow_statement_annual_ticker', table_name='Cash_flow_statement_annual')
    op.drop_table('Cash_flow_statement_annual')
    op.drop_index('ix_Securities_ticker', table_name='Securities')
    op.drop_table('Securities')
    op.drop_index('combo_index_cfa', table_name='Income_statement_annual')
    op.drop_index('combo_index_isa', table_name='Income_statement_annual')
    op.drop_index('ix_Income_statement_annual_date', table_name='Income_statement_annual')
    op.drop_index('ix_Income_statement_annual_ticker', table_name='Income_statement_annual')
    op.drop_table('Income_statement_annual')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Income_statement_annual',
    sa.Column('id', sa.INTEGER(), server_default=sa.text('nextval(\'"Income_statement_annual_id_seq"\'::regclass)'), autoincrement=True, nullable=False),
    sa.Column('date', sa.DATE(), autoincrement=False, nullable=False),
    sa.Column('statement', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('ticker', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('security_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('line_item', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('amount', postgresql.MONEY(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['security_id'], ['Securities.id'], name='Income_statement_annual_security_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='Income_statement_annual_pkey'),
    sa.UniqueConstraint('date', 'ticker', 'line_item', name='unique_entry_isa')
    )
    op.create_index('ix_Income_statement_annual_ticker', 'Income_statement_annual', ['ticker'], unique=False)
    op.create_index('ix_Income_statement_annual_date', 'Income_statement_annual', ['date'], unique=False)
    op.create_index('combo_index_isa', 'Income_statement_annual', ['date', 'ticker', 'line_item'], unique=False)
    op.create_index('combo_index_cfa', 'Income_statement_annual', ['date', 'ticker', 'line_item'], unique=False)
    op.create_table('Securities',
    sa.Column('id', sa.INTEGER(), server_default=sa.text('nextval(\'"Securities_id_seq"\'::regclass)'), autoincrement=True, nullable=False),
    sa.Column('ticker', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('company', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('sector', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('industry', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('country', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='Securities_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_index('ix_Securities_ticker', 'Securities', ['ticker'], unique=False)
    op.create_table('Cash_flow_statement_annual',
    sa.Column('id', sa.INTEGER(), server_default=sa.text('nextval(\'"Cash_flow_statement_annual_id_seq"\'::regclass)'), autoincrement=True, nullable=False),
    sa.Column('date', sa.DATE(), autoincrement=False, nullable=False),
    sa.Column('statement', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('ticker', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('security_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('line_item', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('amount', postgresql.MONEY(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['security_id'], ['Securities.id'], name='Cash_flow_statement_annual_security_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='Cash_flow_statement_annual_pkey'),
    sa.UniqueConstraint('date', 'ticker', 'line_item', name='unique_entry_cfa')
    )
    op.create_index('ix_Cash_flow_statement_annual_ticker', 'Cash_flow_statement_annual', ['ticker'], unique=False)
    op.create_index('ix_Cash_flow_statement_annual_date', 'Cash_flow_statement_annual', ['date'], unique=False)
    op.create_table('Income_statement_quarterly',
    sa.Column('id', sa.INTEGER(), server_default=sa.text('nextval(\'"Income_statement_quarterly_id_seq"\'::regclass)'), autoincrement=True, nullable=False),
    sa.Column('date', sa.DATE(), autoincrement=False, nullable=False),
    sa.Column('statement', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('ticker', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('security_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('line_item', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('amount', postgresql.MONEY(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['security_id'], ['Securities.id'], name='Income_statement_quarterly_security_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='Income_statement_quarterly_pkey'),
    sa.UniqueConstraint('date', 'ticker', 'line_item', name='unique_entry_isq')
    )
    op.create_index('ix_Income_statement_quarterly_ticker', 'Income_statement_quarterly', ['ticker'], unique=False)
    op.create_index('ix_Income_statement_quarterly_date', 'Income_statement_quarterly', ['date'], unique=False)
    op.create_index('combo_index_isq', 'Income_statement_quarterly', ['date', 'ticker', 'line_item'], unique=False)
    op.create_index('combo_index_cfq', 'Income_statement_quarterly', ['date', 'ticker', 'line_item'], unique=False)
    op.create_table('Cash_flow_statement_quarterly',
    sa.Column('id', sa.INTEGER(), server_default=sa.text('nextval(\'"Cash_flow_statement_quarterly_id_seq"\'::regclass)'), autoincrement=True, nullable=False),
    sa.Column('date', sa.DATE(), autoincrement=False, nullable=False),
    sa.Column('statement', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('ticker', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('security_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('line_item', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('amount', postgresql.MONEY(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['security_id'], ['Securities.id'], name='Cash_flow_statement_quarterly_security_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='Cash_flow_statement_quarterly_pkey'),
    sa.UniqueConstraint('date', 'ticker', 'line_item', name='unique_entry_cfq')
    )
    op.create_index('ix_Cash_flow_statement_quarterly_ticker', 'Cash_flow_statement_quarterly', ['ticker'], unique=False)
    op.create_index('ix_Cash_flow_statement_quarterly_date', 'Cash_flow_statement_quarterly', ['date'], unique=False)
    op.create_table('Balance_sheet_quarterly',
    sa.Column('id', sa.INTEGER(), server_default=sa.text('nextval(\'"Balance_sheet_quarterly_id_seq"\'::regclass)'), autoincrement=True, nullable=False),
    sa.Column('date', sa.DATE(), autoincrement=False, nullable=False),
    sa.Column('statement', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('ticker', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('security_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('line_item', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('amount', postgresql.MONEY(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['security_id'], ['Securities.id'], name='Balance_sheet_quarterly_security_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='Balance_sheet_quarterly_pkey')
    )
    op.create_index('ix_Balance_sheet_quarterly_ticker', 'Balance_sheet_quarterly', ['ticker'], unique=False)
    op.create_index('ix_Balance_sheet_quarterly_date', 'Balance_sheet_quarterly', ['date'], unique=False)
    op.create_index('combo_index_bsq', 'Balance_sheet_quarterly', ['date', 'ticker', 'line_item'], unique=False)
    op.create_table('Balance_sheet_annual',
    sa.Column('id', sa.INTEGER(), server_default=sa.text('nextval(\'"Balance_sheet_annual_id_seq"\'::regclass)'), autoincrement=True, nullable=False),
    sa.Column('date', sa.DATE(), autoincrement=False, nullable=False),
    sa.Column('statement', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('ticker', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('security_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('line_item', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('amount', postgresql.MONEY(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['security_id'], ['Securities.id'], name='Balance_sheet_annual_security_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='Balance_sheet_annual_pkey'),
    sa.UniqueConstraint('date', 'ticker', 'line_item', name='unique_entry_bsa')
    )
    op.create_index('ix_Balance_sheet_annual_ticker', 'Balance_sheet_annual', ['ticker'], unique=False)
    op.create_index('ix_Balance_sheet_annual_date', 'Balance_sheet_annual', ['date'], unique=False)
    op.create_index('combo_index_bsa', 'Balance_sheet_annual', ['date', 'ticker', 'line_item'], unique=False)
    op.drop_index(op.f('ix_income_statement_quarterly_ticker'), table_name='income_statement_quarterly')
    op.drop_index(op.f('ix_income_statement_quarterly_date'), table_name='income_statement_quarterly')
    op.drop_index('combo_index_isq', table_name='income_statement_quarterly')
    op.drop_index('combo_index_frq', table_name='income_statement_quarterly')
    op.drop_index('combo_index_cfq', table_name='income_statement_quarterly')
    op.drop_table('income_statement_quarterly')
    op.drop_index(op.f('ix_income_statement_annual_ticker'), table_name='income_statement_annual')
    op.drop_index(op.f('ix_income_statement_annual_date'), table_name='income_statement_annual')
    op.drop_index('combo_index_isa', table_name='income_statement_annual')
    op.drop_index('combo_index_fra', table_name='income_statement_annual')
    op.drop_index('combo_index_cfa', table_name='income_statement_annual')
    op.drop_table('income_statement_annual')
    op.drop_index(op.f('ix_financial_ratios_quarterly_ticker'), table_name='financial_ratios_quarterly')
    op.drop_index(op.f('ix_financial_ratios_quarterly_date'), table_name='financial_ratios_quarterly')
    op.drop_table('financial_ratios_quarterly')
    op.drop_index(op.f('ix_financial_ratios_annual_ticker'), table_name='financial_ratios_annual')
    op.drop_index(op.f('ix_financial_ratios_annual_date'), table_name='financial_ratios_annual')
    op.drop_table('financial_ratios_annual')
    op.drop_index(op.f('ix_cash_flow_statement_quarterly_ticker'), table_name='cash_flow_statement_quarterly')
    op.drop_index(op.f('ix_cash_flow_statement_quarterly_date'), table_name='cash_flow_statement_quarterly')
    op.drop_table('cash_flow_statement_quarterly')
    op.drop_index(op.f('ix_cash_flow_statement_annual_ticker'), table_name='cash_flow_statement_annual')
    op.drop_index(op.f('ix_cash_flow_statement_annual_date'), table_name='cash_flow_statement_annual')
    op.drop_table('cash_flow_statement_annual')
    op.drop_index(op.f('ix_balance_sheet_quarterly_ticker'), table_name='balance_sheet_quarterly')
    op.drop_index(op.f('ix_balance_sheet_quarterly_date'), table_name='balance_sheet_quarterly')
    op.drop_index('combo_index_bsq', table_name='balance_sheet_quarterly')
    op.drop_table('balance_sheet_quarterly')
    op.drop_index(op.f('ix_balance_sheet_annual_ticker'), table_name='balance_sheet_annual')
    op.drop_index(op.f('ix_balance_sheet_annual_date'), table_name='balance_sheet_annual')
    op.drop_index('combo_index_bsa', table_name='balance_sheet_annual')
    op.drop_table('balance_sheet_annual')
    op.drop_index(op.f('ix_securities_table_ticker'), table_name='securities_table')
    op.drop_table('securities_table')
    # ### end Alembic commands ###
