from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import (
    Quotation,
)

from .tasks import (
    search_avaliable_seat_task,
)


@receiver(post_save, sender=Quotation)
def quotation_create_triggering(sender, instance, created, **kwargs):
    if created:
        search_avaliable_seat_task(instance.id, repeat=15, repeat_until=instance.expired_on, creator=instance)

