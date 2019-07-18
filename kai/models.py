from django.db import models

from core.models import ComondBase

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

    def __str__(self):
        return self.quote_id

    def save(self, *args, **kwargs):
        if self.quote_id == 'New':
            self.quote_id = get_quote_code(self)

        super(Quotation, self).save(*args, **kwargs)

