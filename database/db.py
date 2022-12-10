import pathlib

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

BASE_DIR = pathlib.Path(__file__).parent.parent

url = "sqlite:///" + str(BASE_DIR / 'database' / 'app.db.sqlite')
engine = create_engine(url, echo=True)
DBSession = sessionmaker(bind=engine)
session = DBSession()
