import sqlalchemy
import json

from sqlalchemy.orm import sessionmaker
from bookmarket import create_tables, Publisher, Shop, Book, Stock, Sale
from user_data import login, password

database_system = 'postgresql'
database = 'alchemy_db'

if __name__ == '__main__':
    DSN = f'{database_system}://{login}:{password}@localhost:5432/{database}'
    engine = sqlalchemy.create_engine(DSN)
    create_tables(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    # Заполняем нашу БД тестовыми данными
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

    user_input = input("Введите ID издателя или его имя: \n")

    if user_input.isdigit():
        search_id = int(user_input)

    else:
        search_publisher = user_input
        search_id = session.query(Publisher).filter(Publisher.name == search_publisher).all()[0].id

    query = session.query(Sale).join(Sale.stock).join(Stock.shop).join(Stock.book).join(Book.publisher)\
        .filter(Publisher.id == search_id)

    if not query.all():
        print("There is no matches like that")
        session.close()

    for s in query.all():
        print(f'{s.stock.book.title} | {s.stock.shop.name} | {s.price} | {s.date_sale}')

    session.close()
