from django.db import models

class ComondBase(models.Model):
    create_on = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    delete_on = models.DateTimeField(blank=True, null=True)
    is_delete = models.BooleanField(default=False)

    class Meta:
        abstract = True