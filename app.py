import os
import json

import falcon
import base64
import datetime

from sqlalchemy import and_
from db_connect import session
from models.activity_log import ActivityLog
from models.worker import Worker
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, TableStyle
from reportlab.platypus import Table

app = falcon.App(cors_enable=True)


user_accounts = {
    'admin': 'admin'
}


class Autorization(object):
    def __init__(self):
        pass

    def __auth_basic(self, username, password):
        if username in user_accounts and user_accounts[username] == password:
            print('Success')
        else:
            raise falcon.HTTPUnauthorized('Unauthorized', 'Access danied')

    def __call__(self, req, resp, resource, params):
        auth_exp = req.auth.split(' ') if req.auth is not None else (None, None)

        if auth_exp[0] is not None and auth_exp[0].lower() == 'basic':
            auth = base64.b64decode(auth_exp[1]).decode('utf-8').split(':')
            username = auth[0]
            password = auth[1]
            self.__auth_basic(username, password)
        else:
            raise falcon.HTTPNotImplemented('Not Implemented', 'You don\t use the right auth method')


class WorkerApi:
    @falcon.before(Autorization())
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

            resp.body = json.dumps(worker_activity, ensure_ascii=False, indent=4)


class Workers:
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
            l = []

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
                del json_data['payload_by_time']

                pdf_list = list(json_data.values())
                l.append(pdf_list)

            col_list = ['id', 'Name', 'Surname', 'Middle Name', 'Payload']

            l.append(col_list)
            l.reverse()

            BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

            fileName = BASE_DIR + '/dionistask/generated.pdf'

            pdf = SimpleDocTemplate(
                fileName,
                pagesize=letter
            )



            table = Table(l)

            style = TableStyle([
                ('BACKGROUND', (0,0), (5,0), colors.darkcyan),
                ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),

                ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                ('FONTNAME', (0,0), (-1,0), 'Courier-Bold'),
                ('FONTSIZE', (0,0), (-1,0), 14),
                ('BOTTOMPADDING', (0,0), (-1,0), 12),
                ('BACKGROUND', (0,1), (-1,-1), colors.white),
                ('BOX', (0,0), (-1,-1), 0.5, colors.black),
                ('GRID', (0,0), (-1,-1), 0.5, colors.black),
            ])

            table.setStyle(style)

            rowNumb = len(l)
            for i in range(1, rowNumb):
                if i % 2 == 0:
                    bc = colors.darkgray
                else:
                    bc = colors.white
                ts = TableStyle([
                    ('BACKGROUND', (0,i), (-1,i), bc)
                ])

                table.setStyle(ts)

            elems = []
            elems.append(table)
            pdf.build(elems)

            chart_l = []
            chart_d = []
            chart_data = {}
            chart_labels = {}
            for i in worker_activity:
                chart_l.append('{n} {s} {m}'.format(n=i['name'], s=i['surname'], m=i['middle_name']))
                chart_d.append(i['payload_by_date'])

            chart_data.update(dat=chart_d)
            chart_labels.update(label=chart_l)

            worker_activity.append(chart_labels)
            worker_activity.append(chart_data)
            worker_activity.append(fileName)
            worker_activity.reverse()

            print(json.dumps(worker_activity, ensure_ascii=False, indent=4))

            resp.body = json.dumps(worker_activity, ensure_ascii=False, indent=4)


workers = Workers()
workers_api = WorkerApi()
app.add_route('/', workers)
app.add_route('/api', workers_api)
