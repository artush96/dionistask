from random import randint

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.worker import Worker
from models.activity_log import ActivityLog, ActivityStatus, ActivityType
from db_connect import db, session


Session = sessionmaker(db)
session = Session()

names = ['Александр', 'София', 'Мария', 'Максим', 'Михаил', 'Артём', 'Виктория']
surnames = ['Иванов', 'Смирнов', 'Кузнецов', 'Попов', 'Васильев', 'Петров', 'Соколов']
middle_names = ['Александрович', 'Игоревич', 'Сергеевич', 'Геннадьевич', 'Дмитриевич', 'Никитич', 'Ильич']

ids = session.query(Worker).all()

for i in ids:
    print(i.id)

# for i in range(30):
#     ids = Worker.id
#     worker_id = [i for i in ids]
#     print(worker_id)
#     body = randint(000000000, 999999999)
#
#     if i > 30:
#         break