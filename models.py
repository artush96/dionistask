from sqlalchemy import create_engine
from sqlalchemy import Table, Column, String, MetaData, ForeignKey, Integer, Date
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

db_string = 'postgresql:///dionisdb'
db = create_engine(db_string, echo=True)

Base = declarative_base()


class DateTable(Base):
    __tablename__ = 'date_table'

    id = Column(Integer, primary_key=True)
    date = Column(Date)
    worksize = relationship('WorkSizeTable')


class PersonTable(Base):
    __tablename__ = 'person_table'

    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    worksize = relationship('WorkSizeTable')


class WorkSizeTable(Base):
    __tablename__ = 'work_size_table'

    id = Column(Integer, primary_key=True)
    date = Column(Integer, ForeignKey('date_table.id'))
    person = Column(Integer, ForeignKey('person_table.id'))



Session = sessionmaker(db)
session = Session()

Base.metadata.create_all(db)

# Create
doctor_strange = Film(title="Doctor Strange", director="Scott Derrickson", year="2016")
session.add(doctor_strange)
session.commit()


