from background_task import background
from django.template.loader import render_to_string
from django.conf import settings
from django.utils import timezone
from datetime import datetime

from .models import (
    Quotation, TrainOrder
)
from utility.models import (
    Rekening,
)

import requests
import json

URI = settings.KAI_BASE_API
_token = 'Bearer ' + settings.KAI_TOKEN

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
            "date_return": quote.departure_date.strftime('%Y%m%d'),
            "is_return": False,
            "adult": 1,
            "child": 0,
            "infant": 0
        }

        rson = dict()
        c = 0
        try :
            r = requests.post(
                url, 
                data=json.dumps(payload),
                headers = {'source': 'mobile', 'Content-Type': 'application/json'},
                timeout = 10
            )
            # << Add log status

            if r.status_code == requests.codes.ok:
                rson = r.json()

            r.raise_for_status()

            # quote_objs.update(last_record_on=timezone.now())

        except:
            pass

        # << Add log status
        if rson.get('status', 400) == 200:
            for data in rson.get('data', []):
                for i in data.get('schedule', []):
                    if i['subclass'] == quote.subclass and i['train_code'] == quote.train_code and i['available']:
                        c += 1

        if c:
            # Detected any quota...
            quote_objs.update(status=3)

            # ## Process Booking
            booking_order(quote.id) # <<<<


@background(schedule=0)
def booking_order(id):
    quote_objs = Quotation.objects.filter(pk=id, catched=False)
    quote_obj = quote_objs.get()

    t_obj, created = TrainOrder.objects.get_or_create(
        quotation = quote_obj
    )
    # << Add log is already create or not

    if created:
        url = URI + '/booking_b2b'
        payload = {
            "org": quote_obj.dep_code,
            "des": quote_obj.des_code,
            "isreturn": False,
            "dep_date": quote_obj.departure_date.strftime('%Y%m%d'),
            "date_return":"Invalid date",
            "train_no": quote_obj.train_code,
            "train_no_return": 0,
            "num_pax_adult": 1,
            "num_pax_infant": 0,
            "subclass": quote_obj.subclass,
            "subclass_return":"",
            "name": "Anderi setiawan",
            "phone": "082216418455",
            "email": "anderi.setiawan@gmail.com",
            "address": "Gambir, Jakarta",
            "passenger": {
                "adult": [{
                    "name": quote_obj.name,
                    "birthdate": None,
                    "mobile": None,
                    "id_no": quote_obj.id_card
                }],
                "infant": []
            }
        }

        rson = dict()

        try :
            r = requests.post(
                url, 
                data=json.dumps(payload),
                headers = {'source': 'mobile', 'Content-Type': 'application/json', 'Authorization': _token},
                timeout = 10
            )

            #  << Add log status
            if r.status_code == requests.codes.ok:
                rson = r.json()

            r.raise_for_status()

        except :
            pass

        # << Add log status
        if rson.get('status', 400) == 200:
            data = rson['data']['order']

            # Completing Train Order      
            t_obj.book_code = data['book_code']
            t_obj.arrival_code = data['arrival']['code']
            t_obj.arrival_name = data['arrival']['name']
            t_obj.arrival_time = datetime.strptime(data['arrival_date'] + ' ' + data['arrival_time'], '%d%m%Y %H:%M') #
            t_obj.depart_code = data['depart']['code']
            t_obj.depart_name = data['depart']['name']
            t_obj.depart_time = datetime.strptime(data['depart_date'] + ' ' + data['depart_time'], '%d%m%Y %H:%M')#
            t_obj.book_balance = data['book_balance']
            t_obj.book_time = datetime.strptime(data['book_time'], '%d-%m-%Y %H:%M')
            t_obj.class_name = data['class_name']
            t_obj.email = data['contact']['email']
            t_obj.phone = data['contact']['phone']
            t_obj.discount = data['discount']
            t_obj.extra_fee = data['extra_fee']
            t_obj.normal_sales = data['normal_sales']
            t_obj.admin_fee = 15000
            t_obj.pay_code = data['num_code']
            t_obj.pass_name = data['passenger']['adult'][0]['name']
            t_obj.pass_id = data['passenger']['adult'][0]['id_no']
            t_obj.seat_num = data['passenger']['adult'][0]['seat']['seat']
            t_obj.seat_name =  data['seat'][0]
            t_obj.wagon = data['passenger']['adult'][0]['seat']['no_wagon']
            t_obj.train_code = data['train_no']
            t_obj.train_name = data['train_name']
            t_obj.save()

            quote_objs.update(catched=True, status=2)

            # ## Goto Payment Task <<
            payment_tasks(t_obj.id)



def payment_tasks(id):
    objs = TrainOrder.objects.filter(pk=id)
    url = URI + '/add_extra_fee'
    rson = dict()

    a = objs.get()
    try :
        r = requests.post(
            url, 
            data={}, params={'book_code': a.book_code, 'payment_type': 'ATM'},
            headers = {'source': 'mobile', 'Content-Type': 'application/json', 'Authorization': _token},
            timeout = 10
        )

        # << Add log status request
        if r.status_code == requests.codes.ok:
            rson = r.json()


        r.raise_for_status()
        
    except :
        pass

    # << Add log status
    if rson.get('status', 400) == 200:
        data = rson['data']

        objs.update(
            normal_sales = data['normal_sales'],
            extra_fee = data['extra_fee'],
            discount = data['discount'],
            book_balance = data['book_balance'],
            payment_type = data['payment_type'],
            payment_time_limit_str = data['payment_time_limit'],
        )

        try :
            requests.post(
                "https://api.telegram.org/bot{}/sendMessage".format(settings.KAI_TOKEN_NOTIF),
                data = {
                    'chat_id': '@wanotif',
                    'text': 'Catched!!\nBooking Code : {}\n@anderis'.format(a.book_code)
                }, timeout = 10
            )
        except :
            pass
    

@background(schedule=0)
def send_telegram_notif(id):
    train_order_obj = TrainOrder.objects.get(pk=id)
    bank_objs = Rekening.objects.filter(is_active=True)
    
    content = render_to_string(
        'kai/telegram_notif_template_1.html', {'order': train_order_obj, 'banks': bank_objs}
    )
    content = content.replace('</i>\n','</i>')
    try :
        requests.post(
            "https://api.telegram.org/bot{}/sendMessage".format(settings.KAI_TOKEN_NOTIF),
            data = {
                'chat_id': train_order_obj.quotation.telegram,
                'text': content,
                'parse_mode': 'HTML',
            }, timeout = 10
        )
    except :
        pass