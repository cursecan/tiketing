from django.db import models

# Create your models here.

from core.models import ComondBase


class Message(models.Model):
    parse_url = models.SlugField(max_length=30, unique=True)
    title = models.CharField(max_length=200)
    body = models.TextField(max_length=500)

    def __str__(self):
        return self.title
