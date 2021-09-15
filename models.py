# from typing_extensions import ParamSpecArgs
# from datetime import date
# from os import stat_result
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, create_engine #log,
from sqlalchemy.sql.schema import ForeignKey, Index, UniqueConstraint #PrimaryKeyConstraint,
from sqlalchemy.dialects.postgresql import NUMERIC

# CREATE A LOCAL DB, DONT TRY OUT ON RDS YET
Base = declarative_base()

class Security(Base):

    __tablename__   = 'securities_table'
    id              = Column(Integer, primary_key=True, autoincrement=True)
    ticker          = Column(String, index= True)
    company         = Column(String)
    sector          = Column(String)
    industry        = Column(String)
    country         = Column(String)

    def __str__(self):
        return "(f'{self.id}', f'{self.ticker}', f'{self.company}', f'{self.sector}', f'{self.industry}', f'{self.country}')"

    def __repr__(self):
        return (f"{self.id}", f"{self.ticker}", f"{self.company}", f"{self.sector}", f"{self.industry}", f"{self.country}")
        # return "<Book(title='{}', author='{}', pages={}, published={})>"\
                # .format(self.title, self.author, self.pages, self.published)

class Security_table_log(Base):

    __tablename__   = "securities_table_log"
    id              = Column(Integer, primary_key=True, autoincrement=True)
    date            = Column(Date)
    log             = Column(String)
    status          = Column(String)
    added           = Column(String)

class Statements_table_log(Base):

    __tablename__   = "statements_table_log"
    id              = Column(Integer, primary_key=True, autoincrement=True)
    date            = Column(Date)
    log             = Column(String)
    status          = Column(String)
    added           = Column(String)
    days_after_release = Column(Integer)

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