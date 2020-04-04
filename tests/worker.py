from random import randint

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.worker import Worker, WorkerType
from models.meta import Base
from db_connect import db, session



Base.metadata.create_all(db)
# Create
names = ['Александр', 'София', 'Мария', 'Максим', 'Михаил', 'Артём', 'Виктория']
surnames = ['Иванов', 'Смирнов', 'Кузнецов', 'Попов', 'Васильев', 'Петров', 'Соколов']
middle_names = ['Александрович', 'Игоревич', 'Сергеевич', 'Геннадьевич', 'Дмитриевич', 'Никитич', 'Ильич']
types = [WorkerType.COLLECTOR, WorkerType.INSPECTOR]

for i in range(30):
    names_i = randint(0, 6)
    surnames_i = randint(0, 6)
    middle_names_i = randint(0, 6)
    types_i = randint(0, 1)
    deleted_i = randint(0, 1)
    body = randint(000000000, 999999999)

    worker_test = Worker(ean13=body, password='mnbvcxz', name=names[names_i], surname=surnames[surnames_i],
                         middle_name=middle_names[middle_names_i], type=types[types_i], deleted=deleted_i)
    session.add(worker_test)
    session.commit()
    if i > 30:
        break
