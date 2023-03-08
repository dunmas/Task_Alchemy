import sqlalchemy

from sqlalchemy.orm import sessionmaker
from bookmarket import create_tables
from password import password

DSN = f'postgresql://postgres:{password}@localhost:5432/alchemy_db'
engine = sqlalchemy.create_engine(DSN)


create_tables(engine)


Session = sessionmaker(bind=engine)
session = Session()

session.close()
