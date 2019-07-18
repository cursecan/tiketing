from background_task import background
from django.conf import settings

from .models import Quotation

import requests
import json

URI = settings.KAI_BASE_API

@background(schedule=0)
def search_avaliable_seat_task(qid):
    quote_objs = Quotation.objects.filter(
        id = qid,
        closed = False,
        catched = False,
    )

    if quote_objs.exists():
        quote = quote_objs.get()
        
        url = URI + '/get_schedule_v3'
        payload = {
            "org": quote.dep_code,
            "org_is_city": False,
            "des": quote.des_code,
            "des_is_city": False,
            "date": quote.departure_date.strftime('%Y%m%d'),
            "date_return": "",
            "is_return": False,
            "adult": 1,
            "child": 0,
            "infant": 0
        }

        rson = dict()
        c = 0
        try :
            r = requests.post(
                url, data=payload,
                headers = {'source': 'mobile', 'Context-Type': 'application/json'},
                timeout = 10
            )

            if r.status_code == requests.codes.ok:
                rson = r.json()

            r.raise_for_status()

        except:
            pass

        for data in rson.get('data', []):
            for i in data.get('schedule', []):
                if i['subclass'] == quote.subclass and i['train_code'] == quote.train_code and i['available']:
                    c += 1

        if c:
            quote_objs.update(catched=True, status=2)
            try :
                requests.post(
                    "https://api.telegram.org/bot{}/sendMessage".format(settings.KAI_TOKEN_NOTIF),
                    data = {
                        'chat_id': '@wanotif',
                        'text': 'Catched!!\n@anderis'
                    }, timeout = 15
                )
            except :
                pass
            # print('Alert to admin, {} trip chatched...'.format(c))

    
    # Pass