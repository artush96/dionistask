from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

db_string = 'postgresql:///dionisdb'
db = create_engine(db_string, echo=True)

Session = sessionmaker(db)
session = Session()