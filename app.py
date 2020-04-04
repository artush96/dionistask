import json
import unicodedata

import falcon
import datetime

from numpy.core import unicode
from sqlalchemy import extract, and_
from db_connect import session
from models.activity_log import ActivityLog
from models.worker import Worker
from fpdf import FPDF
from collections import deque

app = falcon.App(cors_enable=True)


# def unicode_normalize(s):
#     return unicodedata.normalize('NFKD', s).encode('ascii', 'ignore')

def lt(str):
    return unicode(str, 'latin-1')


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

            pdf = FPDF(orientation='P', unit='mm', format='A4')
            pdf.add_page()
            epw = pdf.w - 2*pdf.l_margin
            col_width = epw / 4

            col_list = ['id', 'Name', 'Surname', 'Middle Name', 'Payload']

            l.append(col_list)
            l.reverse()

            pdf.set_font('Arial', 'B', 14.0)
            pdf.cell(epw, 0.0, 'With more padding', align='C')
            pdf.set_font('Arial', '', 10.0)
            pdf.ln(0.5)

            th = pdf.font_size

            for row in l:
                for datum in row:
                    # try:
                    #     str(datum).encode('latin-1')
                    # except:
                    #     datum = datum.encode('latin-1')
                    pdf.cell(col_width, 2 * th, str(datum), border=1)

                pdf.ln(2 * th)
            # pdf.output('/Users/artush/PycharmProjects/dionistask/generated.pdf')
            print(pdf)

            print(json.dumps(worker_activity, ensure_ascii=False, indent=4))

            resp.body = json.dumps(worker_activity, ensure_ascii=False, indent=4)


obj_request = ObjRequest()
app.add_route('/api', obj_request)
