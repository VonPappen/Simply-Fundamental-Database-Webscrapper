"""removed unecessary columns

Revision ID: 0698c428ee02
Revises: 266d8a640471
Create Date: 2021-09-17 22:33:07.473231

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0698c428ee02'
down_revision = '266d8a640471'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('earnings_release', sa.Column('last_period_N', sa.String(), nullable=True))
    op.add_column('earnings_release', sa.Column('last_period_DB', sa.String(), nullable=True))
    op.drop_column('earnings_release', 'period')
    op.drop_column('earnings_release', 'trend_f_data')
    op.drop_column('earnings_release', 'in_db_f_data')
    op.drop_column('earnings_release', 'in_db')
    op.drop_column('earnings_release', 'trend_ready')
    op.drop_column('earnings_release', 'last_period_db')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('earnings_release', sa.Column('last_period_db', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('earnings_release', sa.Column('trend_ready', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.add_column('earnings_release', sa.Column('in_db', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.add_column('earnings_release', sa.Column('in_db_f_data', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.add_column('earnings_release', sa.Column('trend_f_data', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.add_column('earnings_release', sa.Column('period', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_column('earnings_release', 'last_period_DB')
    op.drop_column('earnings_release', 'last_period_N')
    # ### end Alembic commands ###
