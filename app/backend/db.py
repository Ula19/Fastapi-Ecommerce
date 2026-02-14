from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase


engine = create_engine('sqlite:///ecommerce.db', echo=True)

# типичная форма URL-адреса базы данных для PostgreSQL
# engine = create_engine('postgresql+psycopg2://youuser:youpassword@localhost/youdb')

SessionLocal = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass
