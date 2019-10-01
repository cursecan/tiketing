from background_task import background
from django.conf import settings
from django.utils import timezone

from .models import (
    Booking, Checkout,
)
from .utils import AESCipher

import json, requests, time

_api_base = settings.KAI_API_NEW
_api_token = settings.KAI_TOKEN_NEW


def booking_process(obj):
    cipher = AESCipher()
    url = _api_base + '/rtsngmid/mobile/booking'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': _api_token,
    }
    payload = {
        "propscheduleid": cipher.encrypt(obj.checkin.propscheduleid),
        "tripid": cipher.encrypt(obj.checkin.tripid), 
        "orgid": cipher.encrypt(str(obj.checkin.orgid)), 
        "desid": cipher.encrypt(str(obj.checkin.desid)), 
        "orgcode": cipher.encrypt(obj.checkin.orgcode), 
        "destcode": cipher.encrypt(obj.checkin.destcode), 
        "tripdate": cipher.encrypt(timezone.localtime(obj.checkin.departdatetime).strftime('%Y-%m-%d')), 
        "departdate": cipher.encrypt(timezone.localtime(obj.checkin.departdatetime).strftime('%Y-%m-%d')), 
        "noka": cipher.encrypt(obj.checkin.noka),
        "extrafee": cipher.encrypt('0'),
        "wagonclasscode": cipher.encrypt(obj.checkin.wagonclasscode),
        "wagonclassid": cipher.encrypt(str(obj.checkin.wagonclassid)),
        "customername": cipher.encrypt('Anderi Setiawan'),
        "phone": cipher.encrypt('082216418455'),
        "email": cipher.encrypt('anderi.setiawan@gmail.com'),
        "subclass": cipher.encrypt(obj.checkin.subclass),
        "totpsgadult": cipher.encrypt('1'),
        "totpsgchild": cipher.encrypt('0'),
        "totpsginfant": cipher.encrypt('0'),
        "paxes":[{
            "idnum": cipher.encrypt(obj.passengers.get().passenger_identity),
            "name": cipher.encrypt(obj.passengers.get().passenger_nm),
            "psgtype": cipher.encrypt('A')
        }]
    }
    # print(payload)

    try :
        q = requests.post(
            url, 
            data = json.dumps(payload),
            headers = headers,
            timeout = 10
        )
        if q.status_code == requests.codes.ok:
            qson = q.json()

        q.raise_for_status()
        if qson.get('code') == '00':
            dt_payment = "paycode={},paytypecode=ATM,channelcodepay=MAPP,netamount={},tickettype=R,shiftid=15138,unitcodepay=MID01MAPP,paysource=RTSNG".format(
                qson['payload']['paycode'],
                qson['payload']['netamount'],
            )

            # Process Checkout
            url = _api_base + '/rtsngmid/py_service/mobile/checkout'
            payload = {
                "data": [cipher.encrypt(dt_payment)]
            }

            try :
                r = requests.post(
                    url,
                    data = json.dumps(payload),
                    headers = headers,
                    timeout = 10
                )

                if r.status_code == requests.codes.ok:
                    rson = r.json()

                r.raise_for_status()
                if rson.get('code') == '00':
                    # Checkout Complete
                    Checkout.objects.create(
                        booking=obj, 
                        paycode=rson['payload']['commonPaycode'],
                        net_amount = rson['payload']['aggregateNetAmount']
                    )

                    obj.status = Booking.WAITPAYMENT
                    obj.save()

                    # Telegram Notification
                    try :
                        requests.post(
                            "https://api.telegram.org/bot{}/sendMessage".format(settings.KAI_TOKEN_NOTIF),
                            data = {
                                'chat_id': '@wanotif',
                                'text': '@anderis\n{}-{} / PayCode {}.'.format(obj.checkin.stationnameorg, obj.checkin.stationnamedest, obj.checkout.latest('-id').paycode)
                            }, timeout = 10
                        )
                    except :
                        pass

            except :
                pass
        
    except:
        pass

@background(schedule=0)
def wl_process(id):
    book_objs = Booking.objects.filter(pk=id)
    if book_objs.filter(status=Booking.WAITLIST).exists():
        obj = book_objs.get()
        
        cipher = AESCipher()
        url = _api_base + '/rtsngmid/mobile/getscheduleune'
        headers = {
            'Content-Type': 'application/json',
        }
        payload = {
            "staorigincode": cipher.encrypt(obj.checkin.orgcode), 
            "stadestinationcode": cipher.encrypt(obj.checkin.destcode), 
            "tripdate": cipher.encrypt(timezone.localtime(obj.checkin.departdatetime).strftime("%Y-%m-%d")),
        }

        qson = dict()
        try :
            q = requests.post(url, data=json.dumps(payload), headers=headers, timeout=15)

            if q.status_code == requests.codes.ok:
                qson = q.json()

            # print(q.json())
            q.raise_for_status()
            if qson.get('code') == '00':
                datas = qson.get('payload')

                for i in datas:
                    if i['propscheduleid'] == obj.checkin.propscheduleid and i['availability'] > 0:
                        # process booking
                        booking_process(obj)
                        break

        except :
            pass
