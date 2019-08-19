from django.contrib import admin

from .models import (
    Quotation, TrainOrder
)

from .tasks import (
    send_telegram_notif,
)

admin.site.disable_action('delete_selected')

@admin.register(Quotation)
class QuotationAdmin(admin.ModelAdmin):
    actions = [
        'redetect_action'
    ]
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


    def redetect_action(self, request, queryset):
        filtered_objs = queryset.filter(catched=True)
        r_update = filtered_objs.update(status=1, catched=False)

        if r_update == 1:
            msg_bit = '1 order was'
        else :
            msg_bit = '%s order were' % r_update
        self.message_user(request, '%s successful set to re-detection.' % msg_bit)

    redetect_action.short_description = "Redetect selected records"

@admin.register(TrainOrder)
class TrainOrderAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': [('book_code', 'pay_code')]
        }),
        ('Origin', {
            'fields': [('depart_name', 'depart_code'), 'depart_time']
        }),
        ('Destination', {
            'fields': [('arrival_name', 'arrival_code'), 'arrival_time']
        }),
        ('Cost Informations', {
            'fields': [('normal_sales', 'discount', 'extra_fee'), 'admin_fee']
        })
    )
    readonly_fields = [
        'book_code', 'pay_code', 'status', 'quotation',
        'normal_sales', 'discount', 'extra_fee',
    ]
    list_filter = ['status']
    actions = ['confirm_action', 'cancel_action']
    search_fields = [
        'book_code', 'pass_name', 'pass_id', 'pay_code',
    ]
    list_display = [
        'book_code', 'pay_code',
        'pass_name', 
        'get_depart_display', 'get_arrival_display',
        'depart_time', 'arrival_time',
        'status',
        'payment_time_limit_str',
    ]

    def get_depart_display(self, obj):
        return '{} ({})'.format(obj.depart_name, obj.depart_code)

    def get_arrival_display(self, obj):
        return '{} ({})'.format(obj.arrival_name, obj.arrival_code)

    get_arrival_display.short_description = 'Arrival'
    get_depart_display.short_description = 'Departure'

    def confirm_action(self, request, queryset):
        filtered_objs = queryset.filter(status=1)
        for i in filtered_objs:
            send_telegram_notif(i.id)
            
        r_update = filtered_objs.update(status=2)
        if r_update == 1:
            msg_bit = '1 order was'
        else :
            msg_bit = '%s order were' % r_update
        self.message_user(request, '%s successful mark to waiting payment.' % msg_bit)

    def cancel_action(self, request, queryset):
        filtered_objs = queryset.filter(status=2)
        r_update = filtered_objs.update(status=1)
        if r_update == 1:
            msg_bit = '1 order was'
        else :
            msg_bit = '%s order were' % r_update
        self.message_user(request, '%s successful mark to cancel.' % msg_bit)

    confirm_action.short_description = 'Confirm selected train orders'
    cancel_action.short_description = 'Cancel selected train orders'

    # def get_queryset(self, request):
    #     qs = super(TrainOrderAdmin, self).get_queryset(request)
    #     return qs.filter(status=1)
