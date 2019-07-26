from django.db import models

from core.models import ComondBase
from django.utils import timezone

from .utils import get_quote_code

# class Queue(ComondBase):
#     title = models.CharField(max_length=50)
#     body = models.TextField(max_length=500)
#     origin = models.CharField(max_length=50, blank=True)
#     destination = models.CharField(max_length=50, blank=True)
#     depature_date = models.DateField(blank=True, null=True)
#     train = models.CharField(max_length=50, blank=True)
#     subclass = models.CharField(max_length=50, blank=True)
#     passenger = models.CharField(max_length=50, blank=True)
#     identitas = models.CharField(max_length=50, blank=True)
#     is_valid = models.BooleanField(default=False)

#     def __str__(self):
#         return self.title
        

class Quotation(ComondBase):
    MAN = 1
    WOMAN = 2
    GENDER_LIST = (
        (MAN, "Mr"),
        (WOMAN, "Mrs")
    )

    PROGRESS = 1
    CATCHED = 2
    CLOSED = 0
    STATUS_LIST = (
        (PROGRESS, 'In Progress'),
        (CATCHED, 'Catched'),
        (CLOSED, 'Closed')
    )

    quote_id = models.CharField(max_length=5, editable=False, default='New') 
    dep_code = models.CharField(max_length=10)
    des_code = models.CharField(max_length=10)
    departure_date = models.DateField()
    train_code = models.CharField(max_length=10)
    subclass = models.CharField(max_length=2)
    genre = models.PositiveSmallIntegerField(choices=GENDER_LIST, default=MAN)
    name = models.CharField(max_length=100)
    id_card = models.CharField(max_length=30)
    catched = models.BooleanField(default=False)
    closed = models.BooleanField(default=False)
    expired_on = models.DateTimeField()
    status = models.PositiveIntegerField(choices=STATUS_LIST, default=PROGRESS)

    telegram = models.CharField(max_length=20, blank=True)
    last_record_on = models.DateTimeField(verbose_name='Last Record', default=timezone.now)

    def __str__(self):
        return self.quote_id

    def save(self, *args, **kwargs):
        if self.quote_id == 'New':
            self.quote_id = get_quote_code(self)

        super(Quotation, self).save(*args, **kwargs)



class TrainOrder(ComondBase):
    OPEN = 1
    WAIT_PAY = 2
    PAID = 0
    EXPIRED = 9
    STATUS_LIST = (
        (OPEN, 'Open'),
        (WAIT_PAY, 'Waiting Payment'),
        (PAID, 'Paid'),
        (EXPIRED, 'Expired')
    )

    book_code = models.CharField(max_length=20, blank=True)
    arrival_code = models.CharField(max_length=10, blank=True)
    arrival_name = models.CharField(max_length=255, blank=True)
    arrival_time = models.DateTimeField(blank=True, null=True)
    depart_code = models.CharField(max_length=10, blank=True)
    depart_name = models.CharField(max_length=255, blank=True)
    depart_time = models.DateTimeField(blank=True, null=True)
    book_balance = models.IntegerField(default=0)
    book_time = models.DateTimeField(default=timezone.now)
    class_name = models.CharField(max_length=50, blank=True)
    contact_name = models.CharField(max_length=200, blank=True)
    email = models.EmailField(max_length=200, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    discount = models.IntegerField(default=0)
    extra_fee = models.IntegerField(default=0)
    normal_sales = models.IntegerField(default=0)
    admin_fee = models.IntegerField(default=0)
    pay_code = models.CharField(max_length=50, blank=True)
    pass_name = models.CharField(max_length=200, blank=True)
    pass_id = models.CharField(max_length=50, blank=True)
    seat_num = models.CharField(max_length=10, blank=True)
    seat_name = models.CharField(max_length=50, blank=True)
    wagon = models.CharField(max_length=5, blank=True)
    train_name = models.CharField(max_length=200, blank=True)
    train_code = models.CharField(max_length=10, blank=True)
    quotation = models.ForeignKey(Quotation, on_delete=models.CASCADE, related_name='train_order')
    payment_type = models.CharField(max_length=50, blank=True)
    payment_time_limit_str = models.CharField(max_length=50, blank=True)
    status = models.PositiveSmallIntegerField(choices=STATUS_LIST, default=1)

    def __str__(self):
        return self.book_code



# {"status":200,"message":"","data":{"order":{"depart":{"code":"GMR","name":"Gambir","is_portertaxi":1},"arrival":{"code":"BD","name":"Bandung","is_portertaxi":1},"depart_date_text":"28 July 2019","depart_date":"28072019","depart_time":"05:25","arrival_date_text":"28 July 2019","arrival_date":"28072019","arrival_time":"08:52","train_no":"20","book_code":"9CHFBD","num_code":"9983099416107","contact":{"phone":"082216418455","email":"anderi.setiawan@gmail.com","address":"Gambir, jakarta"},"passenger":{"adult":[{"name":"Mirota Dupo","birthdate":null,"mobile":"0822164184551","id_no":"12452145555","seat":{"class":"PREMIUM_SS","no_wagon":"1","seat":"13C"}}],"infant":[]},"seat":["PREMIUM_SS 1 13C"],"normal_sales":110000,"extra_fee":0,"book_balance":110000,"train_name":"ARGO PARAHYANGAN","class":"K","class_name":"Ekonomi","discount":0,"book_time":"26-07-2019 10:46","subclass":"C","is_near":true}}}