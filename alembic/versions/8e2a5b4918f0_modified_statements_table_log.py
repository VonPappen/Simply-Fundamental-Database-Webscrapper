"""modified statements_table_log

Revision ID: 8e2a5b4918f0
Revises: 0698c428ee02
Create Date: 2021-09-22 17:38:57.013313

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8e2a5b4918f0'
down_revision = '0698c428ee02'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('statements_table_log', sa.Column('ticker', sa.String(), nullable=True))
    op.add_column('statements_table_log', sa.Column('security_id', sa.Integer(), nullable=True))
    op.add_column('statements_table_log', sa.Column('statement', sa.String(), nullable=True))
    op.add_column('statements_table_log', sa.Column('time_format', sa.String(), nullable=True))
    op.create_foreign_key(None, 'statements_table_log', 'securities_table', ['security_id'], ['id'])
    op.drop_column('statements_table_log', 'days_after_release')
    op.drop_column('statements_table_log', 'added')
    op.drop_column('statements_table_log', 'log')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('statements_table_log', sa.Column('log', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('statements_table_log', sa.Column('added', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('statements_table_log', sa.Column('days_after_release', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'statements_table_log', type_='foreignkey')
    op.drop_column('statements_table_log', 'time_format')
    op.drop_column('statements_table_log', 'statement')
    op.drop_column('statements_table_log', 'security_id')
    op.drop_column('statements_table_log', 'ticker')
    # ### end Alembic commands ###