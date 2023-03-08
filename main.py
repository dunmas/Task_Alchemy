import sqlalchemy
import json

from sqlalchemy.orm import sessionmaker
from bookmarket import create_tables, Publisher, Shop, Book, Stock, Sale
from user_data import login, password

database_system = 'postgresql'
database = 'alchemy_db'

DSN = f'{database_system}://{login}:{password}@localhost:5432/{database}'
engine = sqlalchemy.create_engine(DSN)
create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

with open('fixtures/tests_data.json', 'r') as fd:
    data = json.load(fd)

for record in data:
    model = {
        'publisher': Publisher,
        'shop': Shop,
        'book': Book,
        'stock': Stock,
        'sale': Sale,
    }[record.get('model')]
    session.add(model(id=record.get('pk'), **record.get('fields')))
session.commit()

session.close()
