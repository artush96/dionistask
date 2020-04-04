from datetime import datetime, timedelta
from random import randint
from models.worker import Worker
from models.activity_log import ActivityLog, ActivityStatus, ActivityType
from db_connect import session


worker_id = [i.id for i in session.query(Worker).all()]
for i in range(100):
    ids = randint(0, 29)
    body = randint(000000000, 999999999)
    payload = randint(600, 1500)
    datetime_gen = datetime.now() + timedelta(hours=i)

    activity_test = ActivityLog(box_code=body, worker_id=worker_id[ids], payload=payload, type=ActivityType.COLLECT,
                                status=ActivityStatus.SUCCESS, local_time=datetime_gen)
    session.add(activity_test)
    session.commit()
    if i > 100:
        break
