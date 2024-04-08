from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime, JSON, ARRAY, BigInteger, func, text,ForeignKey, desc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from pprint import pprint

load_dotenv()
userName = os.environ.get('POSTGRES_USER')
password = os.environ.get('POSTGRES_PASSWORD')
db = os.environ.get('POSTGRES_DB')
url = os.environ.get('POSTGRES_URL')

print(f'{userName=}')
print(f'{password=}')
print(f'{db=}')

# Создаем подключение к базе данных
engine = create_engine(f'postgresql://{userName}:{password}@{url}:5432/{db}')
# engine = create_engine('mysql://username:password@localhost/games')




 
# Определяем базу данных
Base = declarative_base()


class Table(Base):
    __tablename__ = 'table'
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    date_call = Column(DateTime)
    assigned = Column(Integer)
    url_deal = Column(String)
    duration = Column(Integer)
    ball = Column(Float)
    rez = Column(String)
    good = Column(String)
    bad = Column(String)
    recomend = Column(String)
    answer_gpt = Column(String)
    phone = Column(String)
    answer_gpt_prepare = Column(String)
    type = Column(String)

    

Base.metadata.create_all(engine)
# Base.metadata.update()

Session = sessionmaker(bind=engine)
# session = Session()


def add_table(fields:dict):
    with Session() as session:
        table = Table(**fields)
        session.add(table)
        session.commit()
    return 'ok'


if __name__ ==  '__main__':
    # plan=get_plan_for_month(product='Неликвид', month=1, department='Отдел финансов')
    tab={
        'date_call':datetime.now(),
        'assigned':1,
        'url_deal':'https://profzabor.amocrm.ru/leads/detail/123',
        'duration':10,
        'ball':0.5,
        'rez':'rez',
        'good':'good',
        'bad':'bad',
        'recomend':'recomend',
        'answer_gpt':'answer_gpt',
        'phone':'phone',
        'answer_gpt_prepare':'answer_gpt_prepare',
        'type':'type'
    }
    pass
    # pprint(plan[0].__dict__)
    # pprint(get_now_plan('Лом'))