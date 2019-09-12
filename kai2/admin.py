from django.contrib import admin

from .models import (
    Checkin, Booking, Checkout,
)

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = [
        'checkin', 'status'
    ]

@admin.register(Checkout)
class CheckoutAdmin(admin.ModelAdmin):
    pass