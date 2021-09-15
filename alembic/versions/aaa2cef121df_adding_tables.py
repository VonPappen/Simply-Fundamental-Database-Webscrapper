"""adding tables

Revision ID: aaa2cef121df
Revises: 26d2b27d8c59
Create Date: 2021-09-14 19:07:19.007055

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'aaa2cef121df'
down_revision = '26d2b27d8c59'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Balance_sheet_quarterly',
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
    op.create_index('combo_index_bsq', 'Balance_sheet_quarterly', ['date', 'ticker', 'line_item'], unique=False)
    op.create_index(op.f('ix_Balance_sheet_quarterly_date'), 'Balance_sheet_quarterly', ['date'], unique=False)
    op.create_index(op.f('ix_Balance_sheet_quarterly_ticker'), 'Balance_sheet_quarterly', ['ticker'], unique=False)
    op.create_table('Income_statement_annual',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('date', sa.Date(), nullable=False),
    sa.Column('statement', sa.String(), nullable=True),
    sa.Column('ticker', sa.String(), nullable=True),
    sa.Column('security_id', sa.Integer(), nullable=False),
    sa.Column('line_item', sa.String(), nullable=True),
    sa.Column('amount', postgresql.MONEY(), nullable=True),
    sa.ForeignKeyConstraint(['security_id'], ['Securities.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('date', 'ticker', 'line_item', name='unique_entry_isa')
    )
    op.create_index('combo_index_isa', 'Income_statement_annual', ['date', 'ticker', 'line_item'], unique=False)
    op.create_index(op.f('ix_Income_statement_annual_date'), 'Income_statement_annual', ['date'], unique=False)
    op.create_index(op.f('ix_Income_statement_annual_ticker'), 'Income_statement_annual', ['ticker'], unique=False)
    op.create_table('Income_statement_quarterly',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('date', sa.Date(), nullable=False),
    sa.Column('statement', sa.String(), nullable=True),
    sa.Column('ticker', sa.String(), nullable=True),
    sa.Column('security_id', sa.Integer(), nullable=False),
    sa.Column('line_item', sa.String(), nullable=True),
    sa.Column('amount', postgresql.MONEY(), nullable=True),
    sa.ForeignKeyConstraint(['security_id'], ['Securities.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('date', 'ticker', 'line_item', name='unique_entry_isq')
    )
    op.create_index('combo_index_isq', 'Income_statement_quarterly', ['date', 'ticker', 'line_item'], unique=False)
    op.create_index(op.f('ix_Income_statement_quarterly_date'), 'Income_statement_quarterly', ['date'], unique=False)
    op.create_index(op.f('ix_Income_statement_quarterly_ticker'), 'Income_statement_quarterly', ['ticker'], unique=False)
    op.drop_index('combo_index_bsq', table_name='balance_sheet_quarterly')
    op.drop_index('ix_balance_sheet_quarterly_date', table_name='balance_sheet_quarterly')
    op.drop_index('ix_balance_sheet_quarterly_ticker', table_name='balance_sheet_quarterly')
    op.drop_table('balance_sheet_quarterly')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('balance_sheet_quarterly',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('date', sa.DATE(), autoincrement=False, nullable=False),
    sa.Column('statement', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('ticker', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('security_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('line_item', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('amount', postgresql.MONEY(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['security_id'], ['Securities.id'], name='balance_sheet_quarterly_security_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='balance_sheet_quarterly_pkey'),
    sa.UniqueConstraint('date', 'ticker', 'line_item', name='unique_entry_bsq')
    )
    op.create_index('ix_balance_sheet_quarterly_ticker', 'balance_sheet_quarterly', ['ticker'], unique=False)
    op.create_index('ix_balance_sheet_quarterly_date', 'balance_sheet_quarterly', ['date'], unique=False)
    op.create_index('combo_index_bsq', 'balance_sheet_quarterly', ['date', 'ticker', 'line_item'], unique=False)
    op.drop_index(op.f('ix_Income_statement_quarterly_ticker'), table_name='Income_statement_quarterly')
    op.drop_index(op.f('ix_Income_statement_quarterly_date'), table_name='Income_statement_quarterly')
    op.drop_index('combo_index_isq', table_name='Income_statement_quarterly')
    op.drop_table('Income_statement_quarterly')
    op.drop_index(op.f('ix_Income_statement_annual_ticker'), table_name='Income_statement_annual')
    op.drop_index(op.f('ix_Income_statement_annual_date'), table_name='Income_statement_annual')
    op.drop_index('combo_index_isa', table_name='Income_statement_annual')
    op.drop_table('Income_statement_annual')
    op.drop_index(op.f('ix_Balance_sheet_quarterly_ticker'), table_name='Balance_sheet_quarterly')
    op.drop_index(op.f('ix_Balance_sheet_quarterly_date'), table_name='Balance_sheet_quarterly')
    op.drop_index('combo_index_bsq', table_name='Balance_sheet_quarterly')
    op.drop_table('Balance_sheet_quarterly')
    # ### end Alembic commands ###
