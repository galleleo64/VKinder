# импорты
from pprint import pprint
import sqlalchemy as sq
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import Session

from config import db_url_object
Base = declarative_base()

class Viewed(Base):
    __tablename__ = 'viewed'
    profile_id = sq.Column(sq.Integer, primary_key=True)
    searched_id = sq.Column(sq.Integer, primary_key=True)

def create_table (engine):
    Base.metadata.create_all (engine)

def add_db (engine, profile_id, searched_id):
    with Session(engine) as session:
        data_add_db = Viewed(profile_id=profile_id, searched_id=searched_id)
        session.add(data_add_db)
        session.commit()

def from_db (engine, profile_id, searched_id):
    with Session(engine) as session:
        data_from_db =  session.query(Viewed).filter (Viewed.profile_id==profile_id, Viewed.searched_id==searched_id ).count()
    return data_from_db

engine = sq.create_engine(db_url_object)
create_table (engine)
# add_db (engine, 333, 555)
# pprint (from_db (engine, 333, 545))



# # схема БД
# metadata = MetaData()
# Base = declarative_base()
#
# class Viewed(Base):
#     __tablename__ = 'viewed'
#     profile_id = sq.Column(sq.Integer, primary_key=True)
#     worksheet_id = sq.Column(sq.Integer, primary_key=True)
#
#
# # добавление записи в бд
#
# engine = create_engine(db_url_object)
# Base.metadata.create_all(engine)
# with Session(engine) as session:
#     to_bd = Viewed(profile_id=1, worksheet_id=1)
#     session.add(to_bd)
#     session.commit()
#
# # извлечение записей из БД
#
# engine = create_engine(db_url_object)
# with Session(engine) as session:
#     from_bd = session.query(Viewed).filter(Viewed.profile_id==1).all()
#     for item in from_bd:
#         print(item.worksheet_id)
