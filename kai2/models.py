from django.db import models

from core.models import ComondBase

class Checkin(ComondBase):
    EKO = 'EKO'
    BIS = 'BIS'
    EKS = 'EKS'
    WAGONSELECT = (
        (EKO, 'Ekonomi'),
        (BIS, 'Bisnis'),
        (EKS, 'Eksekutif')
    ) 
    propscheduleid = models.CharField(max_length=10)
    orgcode = models.CharField(max_length=10)
    destcode = models.CharField(max_length=10)
    orgid = models.IntegerField()
    desid = models.IntegerField()
    noka = models.CharField(max_length=10)
    subclass = models.CharField(max_length=10)
    subclassid = models.IntegerField()
    wagonclasscode = models.CharField(max_length=10, choices=WAGONSELECT, default='EKO')
    wagonclassid = models.IntegerField()
    trainname = models.CharField(max_length=100)
    tripid = models.CharField(max_length=10)
    arrivaldatetime = models.DateTimeField()
    departdatetime = models.DateTimeField()
    stationnameorg = models.CharField(max_length=50)
    stationnamedest = models.CharField(max_length=50)
    amount = models.IntegerField()

    def __str__(self):
        return self.propscheduleid

class Booking(ComondBase):
    OPEN = 1
    WAITLIST = 2
    WAITPAYMENT = 3
    PAID = 4
    FINISH = 5
    DROP = 9
    STATESELECT = (
        (OPEN, 'Open Booking'),
        (WAITLIST, 'Waiting List'),
        (WAITPAYMENT, 'Waiting Payment'),
        (PAID, 'Paid'),
        (FINISH, 'Finish'),
        (DROP, 'Drop')
    )
    checkin = models.ForeignKey(Checkin, on_delete=models.PROTECT, related_name='checkin')
    status = models.PositiveSmallIntegerField(choices=STATESELECT, default=OPEN, editable=False)

    class Meta:
        ordering = [
            '-id'
        ]
    def __str__(self):
        return str(self.checkin)


class Passenger(ComondBase):
    booking = models.ForeignKey(Booking, on_delete=models.PROTECT, related_name='passengers', blank=True, null=True)
    passenger_nm = models.CharField(max_length=50)
    passenger_identity = models.CharField(max_length=30)


class Checkout(ComondBase):
    booking = models.ForeignKey(Booking, on_delete=models.PROTECT, related_name='checkout')
    paycode = models.CharField(max_length=20)
    net_amount = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.paycode