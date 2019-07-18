from django.contrib import admin

from .models import (
    Quotation,
)


@admin.register(Quotation)
class QuotationAdmin(admin.ModelAdmin):
    list_display = [
        'quote_id', 'dep_code', 'des_code',
        'status',
        'create_on',
        'last_record_on'
    ]

    fieldsets = [
        (None, {'fields': ['dep_code', 'des_code', 'departure_date']}),
        ('Lokomotif', {'fields': ['train_code', 'subclass']}),
        ('Passenger', {'fields': ['genre', 'name', 'id_card']}),
        ('Additional Info', {'fields': ['expired_on']}),
        (None, {'fields': ['telegram']})
    ]