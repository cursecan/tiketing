from django.db import models

from core.models import ComondBase


class Rekening(ComondBase):
    rek_number = models.CharField(max_length=50)
    account_name = models.CharField(max_length=100, blank=True)
    bank_name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.rek_number
