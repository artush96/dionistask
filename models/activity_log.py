from datetime import datetime
from sqlalchemy.sql.sqltypes import BigInteger, Enum as EnumField, DateTime
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.orm import relation
from models.meta import Base
from models.worker import Worker, WorkerType
from enum import Enum


from db_connect import db

class ActivityType(Enum):
    SELECT_CONTENT_TYPE = 1
    COLLECT = 2
    REVIEW = 3


class ActivityStatus(Enum):
    SUCCESS = 1
    ERROR_CONTENT_TYPE_NOT_FOUND = 2
    ERROR_COLLECTOR_NOT_FOUND = 3
    ERROR_DUPLICATED = 4


class ActivityLog(Base):
    __tablename__ = "activity_log"

    id = Column(BigInteger, primary_key=True, autoincrement=True)

    box_code = Column(BigInteger)
    worker_id = Column(BigInteger, ForeignKey('worker.id'))
    worker = relation("Worker")
    payload = Column(BigInteger)
    type = Column(EnumField(ActivityType))
    status = Column(EnumField(ActivityStatus))

    local_time = Column(DateTime)
    server_time = Column(DateTime, default=datetime.now)

    @hybrid_property
    def collector(self):
        if self.type == ActivityType.COLLECT:
            collector = Worker.query.filter(
                Worker.ean13 == self.payload,
                Worker.type == WorkerType.COLLECTOR
            ).first()
            return collector
        return None

# Base.metadata.create_all(db)