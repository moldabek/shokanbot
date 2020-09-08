from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String

url = 'postgresql://postgres:biba01@localhost:5432/shokan'
engine = create_engine(url, client_encoding='UTF-8', echo=True)
Session = sessionmaker(bind=engine)
Base = declarative_base()
meta = MetaData()


class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    login = Column(String)
    password = Column(String)


def create_table():
    Base.metadata.create_all(engine)


if __name__ == '__main__':
    create_table()
