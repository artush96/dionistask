import json
import falcon
import datetime
from sqlalchemy import extract, and_
from db_connect import session
from models.activity_log import ActivityLog
from models.worker import Worker

app = falcon.App(cors_enable=True)


class ObjRequest:

    def on_get(self, req, resp):
        data = {
            'name': 'Anun',
            'age': '25',
            'type': 'sgxbc',
        }

        resp.body = json.dumps(data, indent=4)

    def on_post(self, req, resp):
        resp.status = falcon.HTTP_200
        data = json.loads(req.stream.read())
        if data['theDate'] != '':
            from_day = datetime.datetime.strptime(data['theDate'], '%Y-%m-%d')
            to_dey = from_day + datetime.timedelta(days=1)
            db_data = session.query(ActivityLog).filter(and_(ActivityLog.local_time >= from_day),
                                                        ActivityLog.local_time < to_dey).all()

            worker_id_list = []
            for i in db_data:
                worker_id_list.append(i.worker_id)

            worker_id_list_filtered = list(dict.fromkeys(worker_id_list))
            worker_activity = []

            for j in worker_id_list_filtered:
                activity_query = session.query(ActivityLog).filter(and_(ActivityLog.local_time >= from_day),
                                                        ActivityLog.local_time < to_dey, ActivityLog.worker_id == j).all()

                worker_query = session.query(Worker).get(j)
                json_data = {}
                all_payload = 0

                payload_list = []
                for q in activity_query:
                    all_payload += int(q.payload)

                    time_payload = {}
                    time_payload['local_time'] = str(q.local_time)
                    time_payload['server_time'] = str(q.server_time)
                    time_payload['payload'] = q.payload
                    payload_list.append(time_payload)

                    json_data['id'] = worker_query.id
                    json_data['name'] = worker_query.name
                    json_data['surname'] = worker_query.surname
                    json_data['middle_name'] = worker_query.middle_name
                    json_data['payload_by_time'] = payload_list
                    json_data['payload_by_date'] = all_payload

                worker_activity.append(json_data)

            print(json.dumps(worker_activity, ensure_ascii=False, indent=4))
            resp.body = json.dumps(worker_activity, ensure_ascii=False, indent=4)


obj_request = ObjRequest()
app.add_route('/api', obj_request)
