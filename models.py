from os import stat_result
from pandas.core.indexes import period
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, create_engine #log,
from sqlalchemy.sql.schema import ForeignKey, Index, UniqueConstraint #PrimaryKeyConstraint,
from sqlalchemy.dialects.postgresql import NUMERIC
from sqlalchemy.sql.sqltypes import Boolean, DateTime

Base = declarative_base()


class Security(Base):

    __tablename__   = 'securities_table'
    id              = Column(Integer, primary_key=True, autoincrement=True)
    ticker          = Column(String, index= True, unique=True)
    company         = Column(String)
    sector          = Column(String)
    industry        = Column(String)
    country         = Column(String)

class Security_table_log(Base):

    __tablename__   = "securities_table_log"
    id              = Column(Integer, primary_key=True, autoincrement=True)
    date            = Column(Date)
    log             = Column(String)
    status          = Column(String)
    added           = Column(String)

class Statements_list(Base):

    __tablename__   = "statements_list_table"
    __table_args__  = (UniqueConstraint("ticker", "date", "statement"),)

    security_id     = Column(Integer, ForeignKey("securities_table.id"))
    ticker          = Column(String,index=True)
    statement       = Column(String)
    date            = Column(Date)
    statement_id    = Column(String, primary_key=True)

class Earnings_release(Base):
    """Updated everyday from Nasdaq"""

    __tablename__   = "earnings_release"
    __table_args__  = (UniqueConstraint("last_period_N", "ticker"),)

    id              = Column(Integer, primary_key=True, autoincrement=True)
    date            = Column(Date, index=True)
    release_date    = Column(Date, index=True)
    ticker          = Column(String,index=True)
    security_id     = Column(Integer, ForeignKey("securities_table.id"))
    last_period_N   = Column(String)
    last_period_DB  = Column(String)
    last_period_M   = Column(String)

class Statements_table_log(Base):

    __tablename__   = "statements_table_log"
    __table_args__  = (UniqueConstraint("ticker", "statement", "time_format", "period"),)

    id              = Column(Integer, primary_key=True, autoincrement=True)
    date            = Column(Date)
    ticker          = Column(String)
    security_id     = Column(Integer, ForeignKey("securities_table.id"))
    statement       = Column(String)
    time_format     = Column(String)
    status          = Column(String)
    period          = Column(String)

class balance_sheet_annual(Base):

    __tablename__   = "balance_sheet_annual"
    __table_args__  = (UniqueConstraint("date", "ticker", "line_item", name="unique_entry_bsa"),)

    id              = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    date            = Column(Date, nullable=False, index=True)
    statement       = Column(String)
    ticker          = Column(String, index=True)
    security_id     = Column(Integer, ForeignKey("securities_table.id"), nullable=False)
    line_item       = Column(String)
    amount          = Column(NUMERIC)
    statement_id    = Column(String, ForeignKey("statements_list_table"))

class balance_sheet_quarterly(Base):

    __tablename__   = "balance_sheet_quarterly"
    __table_args__  = (UniqueConstraint("date", "ticker", "line_item", name="unique_entry_bsq"),)

    id              = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    date            = Column(Date, nullable=False, index=True)
    statement       = Column(String)
    ticker          = Column(String, index=True)
    security_id     = Column(Integer, ForeignKey("securities_table.id"), nullable=False)
    line_item       = Column(String)
    amount          = Column(NUMERIC)
    statement_id    = Column(String, ForeignKey("statements_list_table"))

class income_statement_annual(Base):

    __tablename__   = "income_statement_annual"
    __table_args__  = (UniqueConstraint("date", "ticker", "line_item", name="unique_entry_isa"),)

    id              = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    date            = Column(Date, nullable=False, index=True)
    statement       = Column(String)
    ticker          = Column(String, index=True)
    security_id     = Column(Integer, ForeignKey("securities_table.id"), nullable=False)
    line_item       = Column(String)
    amount          = Column(NUMERIC)
    statement_id    = Column(String, ForeignKey("statements_list_table"))

class income_statement_quarterly(Base):

    __tablename__   = "income_statement_quarterly"
    __table_args__  = (UniqueConstraint("date", "ticker", "line_item", name="unique_entry_isq"),)

    id              = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    date            = Column(Date, nullable=False, index=True)
    statement       = Column(String)
    ticker          = Column(String, index=True)
    security_id     = Column(Integer, ForeignKey("securities_table.id"), nullable=False)
    line_item       = Column(String)
    amount          = Column(NUMERIC)
    statement_id    = Column(String, ForeignKey("statements_list_table"))

class cash_flow_statement_annual(Base):

    __tablename__   = "cash_flow_statement_annual"
    __table_args__  = (UniqueConstraint("date", "ticker", "line_item", name="unique_entry_cfa"),)

    id              = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    date            = Column(Date, nullable=False, index=True)
    statement       = Column(String)
    ticker          = Column(String, index=True)
    security_id     = Column(Integer, ForeignKey("securities_table.id"), nullable=False)
    line_item       = Column(String)
    amount          = Column(NUMERIC)
    statement_id    = Column(String, ForeignKey("statements_list_table"))

class cash_flow_statement_quarterly(Base):

    __tablename__   = "cash_flow_statement_quarterly"
    __table_args__  = (UniqueConstraint("date", "ticker", "line_item", name="unique_entry_cfq"),)

    id              = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    date            = Column(Date, nullable=False, index=True)
    statement       = Column(String)
    ticker          = Column(String, index=True)
    security_id     = Column(Integer, ForeignKey("securities_table.id"), nullable=False)
    line_item       = Column(String)
    amount          = Column(NUMERIC)
    statement_id    = Column(String, ForeignKey("statements_list_table"))

class financial_ratios_annual(Base):

    __tablename__   = "financial_ratios_annual"
    __table_args__  = (UniqueConstraint("date", "ticker", "line_item", name="unique_entry_fra"),)

    id              = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    date            = Column(Date, nullable=False, index=True)
    statement       = Column(String)
    ticker          = Column(String, index=True)
    security_id     = Column(Integer, ForeignKey("securities_table.id"), nullable=False)
    line_item       = Column(String)
    amount          = Column(NUMERIC)
    statement_id    = Column(String, ForeignKey("statements_list_table"))

class financial_ratios_quarterly(Base):

    __tablename__   = "financial_ratios_quarterly"
    __table_args__  = (UniqueConstraint("date", "ticker", "line_item", name="unique_entry_frq"),)

    id              = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    date            = Column(Date, nullable=False, index=True)
    statement       = Column(String)
    ticker          = Column(String, index=True)
    security_id     = Column(Integer, ForeignKey("securities_table.id"), nullable=False)
    line_item       = Column(String)
    amount          = Column(NUMERIC)
    statement_id    = Column(String, ForeignKey("statements_list_table"))

combo_index_bsa     = Index(
    'combo_index_bsa',
    balance_sheet_annual.date,
    balance_sheet_annual.ticker,
    balance_sheet_annual.line_item)

combo_index_bsq     = Index(
    'combo_index_bsq',
    balance_sheet_quarterly.date,
    balance_sheet_quarterly.ticker,
    balance_sheet_quarterly.line_item)

combo_index_isq     = Index(
    'combo_index_isq',
    income_statement_quarterly.date,
    income_statement_quarterly.ticker,
    income_statement_quarterly.line_item)

combo_index_isa     = Index(
    'combo_index_isa',
    income_statement_annual.date,
    income_statement_annual.ticker,
    income_statement_annual.line_item)

combo_index_cfq     = Index(
    'combo_index_cfq',
    income_statement_quarterly.date,
    income_statement_quarterly.ticker,
    income_statement_quarterly.line_item)

combo_index_cfa     = Index(
    'combo_index_cfa',
    income_statement_annual.date,
    income_statement_annual.ticker,
    income_statement_annual.line_item)

combo_index_frq     = Index(
    'combo_index_frq',
    income_statement_quarterly.date,
    income_statement_quarterly.ticker,
    income_statement_quarterly.line_item)

combo_index_fra     = Index(
    'combo_index_fra',
    income_statement_annual.date,
    income_statement_annual.ticker,
    income_statement_annual.line_item)