from sqlalchemy import create_engine
from config import DATABASE_URI
from models import Base, Security
from sqlalchemy.orm import sessionmaker
import datetime
from scrapping_sources.Finviz import Finviz

engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)


def recreate_database():
    # Delete all models
    Base.metadata.drop_all(engine)
    # Create all models
    Base.metadata.create_all(engine)

# Individual session
s = Session()


# Always make sure that the session is closed after using it
# s.close()
# Keep sessions open will also prevent you from recreating the database.
# If you see the recreate hanging, this is probably why.

# Inserting rows
# book = Security(
#     title           = "Deep Learning",
#     author          = "Ian Goodfellow",
#     pages           = 775,
#     published  = datetime.datetime(2016,11,18)
# )

# adding rows to database
# s.add(book)
# s.commit()
s.close()

# print(s.query(Book).all())