from config import DATABASE_URI
from sqlalchemy import create_engine
from models import Base

engine = create_engine(DATABASE_URI)
Base.metadata.create_all(engine)