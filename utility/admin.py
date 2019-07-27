from django.contrib import admin

from .models import (
    Rekening,
)


@admin.register(Rekening)
class RekeningAdmin(admin.ModelAdmin):
    pass