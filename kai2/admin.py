from django.contrib import admin
from background_task.models import Task

from .models import (
    Checkin, Booking, Checkout,
)

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    actions = [
        'delete_realte_runingbgtask',
    ]
    list_display = [
        'checkin',
        'trip_display',
        'tripdate_display',
        'net_amount_display',
        'paycode_display',
        'status'
    ]

    def trip_display(self, obj):
        return '{} - {}'.format(obj.checkin.stationnameorg, obj.checkin.stationnamedest)

    def tripdate_display(self, obj):
        return obj.checkin.departdatetime

    def net_amount_display(self, obj):
        try :
            return obj.checkout.latest('-id').net_amount
        except:
            return 0

    def paycode_display(self, obj):
        try :
            return obj.checkout.latest('-id').paycode
        except :
            return None

    def delete_realte_runingbgtask(self, request, queryset):
        for i in queryset:
            Task.objects.filter(verbose_name='wl-{}'.format(i.id)).delete()



    delete_realte_runingbgtask.short_description = 'Delete selected relate backgroud task'
    trip_display.short_description = 'Trayek'
    tripdate_display.short_description = 'Depart Time'
    net_amount_display.short_description = 'Net Amount'
    paycode_display.short_description = 'Payment Code'
# @admin.register(Checkout)
# class CheckoutAdmin(admin.ModelAdmin):
#     pass