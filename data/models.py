from sqlalchemy import create_engine, MetaData, ForeignKey, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, DateTime
from config import url

url = url
engine = create_engine(url, client_encoding='UTF-8', echo=True)
Session = sessionmaker(bind=engine)
Base = declarative_base()
meta = MetaData()


class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String)
    login = Column(String)


class Score(Base):
    __tablename__ = 'scores'
    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String, nullable=False)
    score = Column(Integer)
    date = Column(DateTime, default=text('NOW()'))
    user = Column(ForeignKey(Users))


def create_table():
    Base.metadata.create_all(engine)


if __name__ == '__main__':
    create_table()
