from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.generic import TemplateView, View, DetailView, ListView
from django.template.loader import render_to_string

from .utils import AESCipher
from .models import (
    Checkin, Booking,
)
from .forms import (
    PassengerForm,
)
from .tasks import (
    wl_process,
)

import requests, json



class HomeTemplateView(TemplateView):
    template_name = 'kai2/index.html'


def cityListJson(request):
    rson = []
    try:
        r = requests.get('https://booking.kai.id/api/stations2', timeout=10)
        if r.status_code == requests.codes.ok:
            rson = r.json()
    except :
        pass


    data = {
        'results': list(map(lambda x: dict(x, value=x['code']), rson))
    }
    
    return JsonResponse(data)


def scheduleListJson(request):
    data = dict()
    url = 'http://midsvc-rtsng.kai.id:8111'
    key = 'Bearer eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIkMnkkMTAkVVNNQ2pvdUlEV2lNWU9sMFFvemIxT3plbi51N2F1cHlUdTlIYnREcVJ1Zmg2Qlo1VlVnYlN8YW5kZXJpLnNldGlhd2FuQGdtYWlsLmNvbXwwODIyMTY0MTg0NTV8MTE0NDg3OCIsImV4cCI6MTU3MzgzMjc5NywiaXNzIjoiaHR0cHM6Ly9rYWlhY2Nlc3MxMS5rYWkuaWQvYXBpL3YxMi9hdXRoL2xvZ2luIn0.G847ZqfYfgx8CahArNdLP1LgkZsQS1n66sohSW1VbOUUxM7i2uRah1NREpce4PgGbrMjrbOV8YFG-eHk10lJnw'
    org = request.POST.get('org')
    dst = request.POST.get('dst')
    depart = request.POST.get('depart')
    y,m,d = depart.split('-')

    cipher = AESCipher('telo_pendem_tele')
    payload = {
        "staorigincode": cipher.encrypt(org),
        "stadestinationcode": cipher.encrypt(dst),
        "tripdate": cipher.encrypt(y+'-'+m.zfill(2)+'-'+d.zfill(2)),
    }
    content = {'origin': org, 'destination': dst, 'dep':depart, 'payloads': []}
    try :
        r = requests.post(
            url = url + '/rtsngmid/mobile/getscheduleune',
            data = json.dumps(payload),
            headers = {'Content-Type': 'application/json'},
            timeout=15
        )
        
        if r.status_code == requests.codes.ok:
            rson = r.json()
            content['payloads'] = list(map(lambda x: dict(x, amount=x['fares'][0]['amount']), rson['payload']))
            # print(rson['payload'])
    except :
        pass

    data['html'] = render_to_string(
        'kai2/include/kai-schedule-list.html',
        content, request=request
    )

    return JsonResponse(data)

def checkinPostView(request):
    if request.method == 'POST':
        propscheduleid=request.POST.get('propscheduleid')
        orgcode=request.POST.get('orgcode')
        orgid=request.POST.get('orgid')
        destcode=request.POST.get('destcode')
        desid=request.POST.get('desid')
        noka=request.POST.get('noka')
        subclass=request.POST.get('subclass')
        subclassid=request.POST.get('subclassid')
        wagonclasscode=request.POST.get('wagonclasscode')
        wagonclassid=request.POST.get('wagonclassid')
        trainname=request.POST.get('trainname')
        tripid=request.POST.get('tripid')
        arrivaldatetime=request.POST.get('arrivaldatetime')
        departdatetime=request.POST.get('departdatetime')
        stationnameorg=request.POST.get('stationnameorg')
        stationnamedest=request.POST.get('stationnamedest')
        amount=request.POST.get('amount')
    
        obj = Checkin.objects.create(
            propscheduleid=propscheduleid, orgcode=orgcode,
            orgid=orgid, destcode=destcode, desid=desid,
            noka=noka, subclass=subclass, subclassid=subclassid, wagonclasscode=wagonclasscode, wagonclassid=wagonclassid,
            trainname=trainname, tripid=tripid, arrivaldatetime=arrivaldatetime, departdatetime=departdatetime,
            stationnameorg=stationnameorg, stationnamedest=stationnamedest, amount=amount
        )
        booking_obj = Booking.objects.create(
            checkin=obj,
        )
        return redirect('kai2:booking', booking_obj.id)

    
class TemplateDetailCheckin(DetailView):
    template_name = 'kai2/checkin.html'
    model = Checkin


class TemplateBookingView(DetailView):
    template_name = 'kai2/booking.html'
    model = Booking
    # queryset = Booking.objects.filter(status=Booking.OPEN)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['form'] = PassengerForm()
        return context

def passengerPostView(request, id): # booking id
    data = dict()
    form = PassengerForm(request.POST or None)
    book_obj = get_object_or_404(Booking, pk=id)
    if request.method == 'POST':
        if form.is_valid():
            instance = form.save(commit=False)
            instance.booking = book_obj
            instance.save()
            data['form_is_valid'] = True

        else :
            data['form_is_valid'] = False

    content = {
        'form': form,
        'object': book_obj,
    }
    data['html'] = render_to_string(
        'kai2/include/passenger-form.html', content, request=request
    )
    return JsonResponse(data)


def waitingListActionView(request, id): # booking id
    booking_obj = get_object_or_404(Booking, pk=id, status=Booking.OPEN)
    data = dict()
    data['form_is_valid'] = False
    if request.method == 'POST':
        booking_obj.status = Booking.WAITLIST
        booking_obj.save()
        data['form_is_valid'] = True

        wl_process(booking_obj.id, verbose_name='wl-{}'.format(booking_obj.id), creator=booking_obj, repeat=30, repeat_until=booking_obj.checkin.departdatetime)

    data['html'] = render_to_string(
        'kai2/include/wl-action.html', {'object': booking_obj}, request=request
    )
    return JsonResponse(data)


class BookedHistoryListView(ListView):
    template_name = 'kai2/booking-list-history.html'
    model = Booking