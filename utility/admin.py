from django.contrib import admin

from .models import (
    Rekening,
)


# @admin.register(Rekening)
# class RekeningAdmin(admin.ModelAdmin):
#     actions = ['active_action', 'inactive_action']
#     list_filter = ['is_active']
#     list_display = [
#         'rek_number', 'bank_name', 'account_name', 'is_active'
#     ]

#     def active_action(self, request, queryset):
#         c_update = queryset.update(is_active=True)
#         if c_update == 1:
#             bit_msg = '%s record was' % c_update
#         else :
#             bit_msg = '%s record were' % c_update

#         self.message_user(request, '{} success mark to active.'.format(bit_msg))

#     def inactive_action(self, request, queryset):
#         c_update = queryset.update(is_active=False)

#         if c_update == 1:
#             bit_msg = '%s record was' % c_update
#         else :
#             bit_msg = '%s record were' % c_update

#         self.message_user(request, '{} success mark to inactive.'.format(bit_msg))

#     active_action.short_description = "Activate selected rekening"
#     inactive_action.short_description = "Non acivate selected rekening"